# Hot RunPod bench image: CUDA runtime, five Whisper weights, 99 mix wavs, aliases.
# Build: docker build -t verse-cue-bench:hot .
# Run (GPU): docker run --gpus all -e WORKERS=16 verse-cue-bench:hot bench --limit 99 --workers 16
#
# Blackwell (RTX PRO 6000): stock CTranslate2 often lacks sm_120. Warmup must pass
# before you start the 3h clock. Prefer Ada (4090 / 6000 Ada / L40S) if warmup fails.
# compute_type is float16 (int8 dies on many Blackwell wheels).

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
    WORKERS=16 \
    SONG_LIMIT=99 \
    COMPUTE_TYPE=float16 \
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
