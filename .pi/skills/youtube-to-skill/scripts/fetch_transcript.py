# Copyright (C) 2026 Austin Bakanec
"""Fetch a YouTube transcript and metadata for skill creation.

Usage:
  python scripts/fetch_transcript.py <url> [--cookies FILE] [--cookies-from-browser NAME] [--outdir DIR]

Exit codes:
  0  transcript written
  2  blocked or unavailable (see FETCH_STATUS in output)
  3  usage error
"""

from __future__ import annotations

import re
import sys
import html
import json
import asyncio
from pathlib import Path
import argparse
import contextlib
from dataclasses import dataclass
import urllib.request

VIDEO_ID_RE = re.compile(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})")
BOT_MARKERS = ("sign in to confirm", "not a bot", "login_required")
UNAVAILABLE_MARKERS = ("video unavailable", "this video is unavailable", "private video")
TAG_RE = re.compile(r"<[^>]+>")
INLINE_TS_RE = re.compile(r"<\d\d:\d\d:\d\d\.\d+>")
SUBTITLE_LANGS = "en.*"
SOCKET_TIMEOUT = 20
RETRIES = 2
FETCH_TIMEOUT = 180


@dataclass(frozen=True)
class CommandResult:
    """Captured result data from one yt-dlp process."""

    returncode: int
    stdout: str
    stderr: str


def emit(message: str) -> None:
    """Write one status line to the script output."""
    sys.stdout.write(f"{message}\n")


def extract_video_id(url: str) -> str | None:
    """Extract the 11-char video id from a YouTube URL.

    Returns
    -------
    str or None
        The video id, or None when the URL is not a YouTube video URL.
    """
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url.strip()):
        return url.strip()
    match = VIDEO_ID_RE.search(url)
    return match.group(1) if match else None


def ytdlp_command(workdir: Path, url: str, extra: list[str]) -> list[str]:
    """Build the yt-dlp command line.

    Returns
    -------
    list[str]
        The command as an argument list.
    """
    return [
        "uvx",
        "yt-dlp",
        "--skip-download",
        "--no-playlist",
        "--socket-timeout",
        str(SOCKET_TIMEOUT),
        "--retries",
        str(RETRIES),
        "--write-info-json",
        "--sub-format",
        "vtt",
        "--js-runtimes",
        "node",
        "--remote-components",
        "ejs:github",
        "-o",
        str(workdir / "%(id)s.%(ext)s"),
        *extra,
        url,
    ]


async def run_ytdlp(command: list[str]) -> CommandResult:
    """Run yt-dlp through uvx without a shell.

    Returns
    -------
    CommandResult
        Captured process output and exit status.
    """
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=FETCH_TIMEOUT)
    except TimeoutError:
        process.kill()
        await process.communicate()
        return CommandResult(returncode=1, stdout="", stderr="yt-dlp timed out")
    return CommandResult(
        returncode=process.returncode if process.returncode is not None else 1,
        stdout=stdout.decode(errors="replace"),
        stderr=stderr.decode(errors="replace"),
    )


def find_vtt(workdir: Path, video_id: str) -> Path | None:
    """Find the first .vtt subtitle file for the video.

    Returns
    -------
    Path or None
        The subtitle file path, or None when no subtitle exists.
    """
    for path in workdir.iterdir():
        if path.name.startswith(video_id) and path.name.endswith(".vtt"):
            return path
    return None


def clean_line(line: str) -> str:
    """Remove inline timestamps, tags, and entities from one caption line.

    Returns
    -------
    str
        The cleaned caption text.
    """
    cleaned = INLINE_TS_RE.sub("", line)
    cleaned = TAG_RE.sub("", cleaned)
    return html.unescape(cleaned).strip()


def clean_vtt(text: str) -> str:
    """Turn a VTT transcript into plain text without timestamps or tags.

    Returns
    -------
    str
        One caption per line, with duplicated captions removed.
    """
    cues: list[str] = []
    seen_timing = False
    for block in text.split("\n\n"):
        lines = [line for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        if not seen_timing:
            if "-->" not in lines[0]:
                continue
            seen_timing = True
        cue = " ".join(clean_line(line) for line in lines if "-->" not in line)
        if cue and (not cues or cue != cues[-1]):
            cues.append(cue)
    return "\n".join(cues)


def fetch_oembed(video_id: str) -> dict:
    """Fetch the video title and channel from the oEmbed endpoint.

    Returns
    -------
    dict
        The oEmbed JSON payload.
    """
    url = "https://www.youtube.com/oembed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D" + video_id + "&format=json"
    with urllib.request.urlopen(url, timeout=SOCKET_TIMEOUT) as response:
        return json.loads(response.read().decode("utf-8"))


def read_info(workdir: Path, video_id: str) -> dict:
    """Load the yt-dlp info.json payload for the video.

    Returns
    -------
    dict
        The info payload, or an empty dict when the file is absent.
    """
    path = workdir / f"{video_id}.info.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_metadata(workdir: Path, video_id: str, info: dict, oembed: dict | None) -> None:
    """Write metadata.json with chapter and subtitle data."""
    chapters = [
        {"start_time": chapter.get("start_time"), "title": chapter.get("title")}
        for chapter in info.get("chapters") or []
    ]
    metadata = {
        "video_id": video_id,
        "title": info.get("title") or (oembed or {}).get("title"),
        "channel": info.get("channel") or info.get("uploader") or (oembed or {}).get("author_name"),
        "duration_seconds": info.get("duration"),
        "upload_date": info.get("upload_date"),
        "description": (info.get("description") or "")[:2000],
        "chapters": chapters,
        "manual_subtitle_languages": sorted((info.get("subtitles") or {}).keys()),
        "auto_caption_languages": sorted((info.get("automatic_captions") or {}).keys()),
    }
    path = workdir / "metadata.json"
    path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def detect_status(result: CommandResult) -> str | None:
    """Classify a failed yt-dlp run.

    Returns
    -------
    str or None
        The status name, or None when the run succeeded.
    """
    if result.returncode == 0:
        return None
    output = (result.stdout + result.stderr).lower()
    if any(marker in output for marker in BOT_MARKERS):
        return "BLOCKED"
    if any(marker in output for marker in UNAVAILABLE_MARKERS):
        return "UNAVAILABLE"
    return "FAILED"


def handle_abort(workdir: Path, video_id: str, status: str) -> int:
    """Record partial metadata, explain the status, and return exit code 2.

    Returns
    -------
    int
        The exit code 2.
    """
    oembed = None
    with contextlib.suppress(Exception):
        oembed = fetch_oembed(video_id)
    write_metadata(workdir, video_id, {}, oembed)
    if oembed:
        emit(f"TITLE: {oembed.get('title')}")
        emit(f"CHANNEL: {oembed.get('author_name')}")
    emit(f"FETCH_STATUS: {status}")
    if status == "BLOCKED":
        emit("REASON: YouTube blocks this IP without login cookies.")
        emit("NEXT: retry with --cookies or --cookies-from-browser, or paste the transcript.")
    elif status == "UNAVAILABLE":
        emit("REASON: the video is private, removed, or region-locked.")
    return 2


def handle_failed(result: CommandResult) -> int:
    """Print the yt-dlp error output and return exit code 2.

    Returns
    -------
    int
        The exit code 2.
    """
    emit("FETCH_STATUS: FAILED")
    emit(result.stdout[-800:])
    emit(result.stderr[-800:])
    return 2


def finish(workdir: Path, video_id: str, vtt_path: Path) -> int:
    """Write the clean transcript and metadata, then print the summary.

    Returns
    -------
    int
        The exit code 0.
    """
    info = read_info(workdir, video_id)
    transcript = clean_vtt(vtt_path.read_text(encoding="utf-8"))
    (workdir / "transcript.txt").write_text(transcript + "\n", encoding="utf-8")
    write_metadata(workdir, video_id, info, None)
    emit(f"VIDEO_ID: {video_id}")
    emit(f"TITLE: {info.get('title')}")
    emit(f"CHANNEL: {info.get('channel') or info.get('uploader')}")
    emit(f"DURATION_SECONDS: {info.get('duration')}")
    emit(f"CHAPTERS: {len(info.get('chapters') or [])}")
    emit(f"TRANSCRIPT_WORDS: {len(transcript.split())}")
    emit(f"TRANSCRIPT_PATH: {workdir / 'transcript.txt'}")
    emit(f"METADATA_PATH: {workdir / 'metadata.json'}")
    emit("FETCH_STATUS: OK")
    return 0


async def attempt(
    workdir: Path,
    video_id: str,
    url: str,
    cookie_args: list[str],
    *,
    auto: bool,
) -> tuple[int | None, Path | None]:
    """Run one subtitle fetch attempt.

    Returns
    -------
    tuple[int | None, Path | None]
        The exit code and the VTT path. The exit code is None when the
        attempt can proceed to the next fallback.
    """
    flag = "--write-auto-subs" if auto else "--write-subs"
    command = ytdlp_command(workdir, url, [*cookie_args, flag, "--sub-langs", SUBTITLE_LANGS])
    result = await run_ytdlp(command)
    status = detect_status(result)
    if status is not None:
        if status == "FAILED":
            return handle_failed(result), None
        return handle_abort(workdir, video_id, status), None
    return None, find_vtt(workdir, video_id)


async def run_fetch(workdir: Path, video_id: str, url: str, cookie_args: list[str]) -> int:
    """Fetch subtitles and metadata, trying manual captions first.

    Returns
    -------
    int
        The process exit code.
    """
    for auto in (False, True):
        code, vtt_path = await attempt(workdir, video_id, url, cookie_args, auto=auto)
        if code is not None:
            return code
        if vtt_path is not None:
            return finish(workdir, video_id, vtt_path)
    emit("FETCH_STATUS: NO_CAPTIONS")
    emit("NEXT: retry with --cookies or --cookies-from-browser, or paste the transcript.")
    return 2


def build_cookie_args(args: argparse.Namespace) -> list[str]:
    """Convert the cookie options into yt-dlp arguments.

    Returns
    -------
    list[str]
        The yt-dlp cookie arguments.
    """
    if args.cookies:
        return ["--cookies", args.cookies]
    if args.cookies_from_browser:
        return ["--cookies-from-browser", args.cookies_from_browser]
    return []


def main() -> int:
    """Run the fetch workflow.

    Returns
    -------
    int
        The process exit code.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="YouTube URL or 11-char video id")
    parser.add_argument("--cookies", help="Netscape cookies.txt file exported from a browser")
    parser.add_argument("--cookies-from-browser", help="Browser name, for example chrome")
    parser.add_argument("--outdir", help="Output directory (default tmp/youtube-to-skill/<id>)")
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    if video_id is None:
        emit("FETCH_STATUS: NOT_YOUTUBE_URL")
        return 3
    workdir = Path(args.outdir or f"tmp/youtube-to-skill/{video_id}")
    workdir.mkdir(parents=True, exist_ok=True)
    return asyncio.run(run_fetch(workdir, video_id, args.url, build_cookie_args(args)))


if __name__ == "__main__":
    raise SystemExit(main())
