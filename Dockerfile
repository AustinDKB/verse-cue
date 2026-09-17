# Hot RunPod bench: 9 copies of each Whisper size (~56.5GB / 60GB cap), batched decode.
# Build: docker build --platform=linux/amd64 -t verse-cue-bench:hot .
# Prefer Ampere/Ada 80GB. Blackwell CT2 often lacks sm_120.

FROM nvidia/cuda:12.6.3-cudnn-runtime-ubuntu24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3.12 python3.12-venv ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/app/.cache/huggingface \
    REPLICAS_PER_MODEL=9 \
    WHISPER_NUM_WORKERS=4 \
    BATCH_SIZE=16 \
    SONG_LIMIT=99 \
    COMPUTE_TYPE=float16 \
    BUDGET_S=6900 \
    HEADROOM_FRAC=0 \
    VRAM_CAP_MB=61440 \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    UV_NO_DEV=1

COPY pyproject.toml uv.lock README.md ./
COPY verse_cue.py harvest.py verse-cue.toml ./
RUN uv sync --frozen --no-dev --extra cuda --python python3.12

COPY scripts/gpu_models.py scripts/gpu_prefetch.py scripts/
RUN uv run python scripts/gpu_prefetch.py

COPY scripts/ ./scripts/
COPY harvest.py ./
COPY aliases.json songs.txt ./
COPY data/ ./data/
RUN chmod +x scripts/gpu_entry.sh \
    && uv run python -c "from pathlib import Path; import harvest as h; print('songs', len(h.songs(10_000)))"

ENTRYPOINT ["./scripts/gpu_entry.sh"]
CMD ["bench"]
