"""Fail fast if CUDA/faster-whisper cannot transcribe on this GPU. Run before the 3h bench."""

import subprocess
import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent)]

import numpy as np
from faster_whisper import WhisperModel

from gpu_models import MODELS


def main() -> None:
    smi = subprocess.run(["nvidia-smi"], check=False)
    if smi.returncode != 0:
        print("nvidia-smi failed", file=sys.stderr)
        sys.exit(1)
    dummy = np.zeros(16000 * 4, dtype=np.float32)
    for name in MODELS:
        model = WhisperModel(name, device="cuda", compute_type="float16")
        segments, _ = model.transcribe(
            dummy, language="en", beam_size=1, word_timestamps=True, vad_filter=False, condition_on_previous_text=False
        )
        list(segments)
        print("cuda ok", name, flush=True)
    print("warmup passed", flush=True)


if __name__ == "__main__":
    main()
