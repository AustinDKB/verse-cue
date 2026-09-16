"""Download CTranslate2 weights into $HF_HOME during docker build (CPU, no GPU required)."""

import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent)]

from faster_whisper import WhisperModel

from gpu_models import MODELS

if __name__ == "__main__":
    for name in MODELS:
        WhisperModel(name, device="cpu", compute_type="int8")
        print("cached", name, flush=True)
