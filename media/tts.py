"""Render media/narration.txt with Kokoro. Run from repo root."""

from pathlib import Path
import wave

import numpy as np
from kokoro_onnx import Kokoro

ROOT = Path(__file__).resolve().parent
TEXT = (ROOT / "narration.txt").read_text().strip()
MODEL = ROOT / "models" / "kokoro-v1.0.onnx"
VOICES = ROOT / "models" / "voices-v1.0.bin"


def main() -> None:
    kokoro = Kokoro(str(MODEL), str(VOICES))
    samples, sr = kokoro.create(TEXT, voice="af_heart")
    pcm = (np.clip(samples, -1, 1) * 32767).astype(np.int16)
    out = ROOT / "narration.wav"
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())
    print(out, len(samples) / sr, "s")


if __name__ == "__main__":
    main()
