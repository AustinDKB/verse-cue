#!/bin/bash
set -euo pipefail
cd /app
case "${1:-bench}" in
  warmup) exec uv run python scripts/gpu_warmup.py ;;
  prefetch) exec uv run python scripts/gpu_prefetch.py ;;
  bench)
    shift
    uv run python scripts/gpu_warmup.py
    exec uv run python scripts/gpu_bench.py "$@"
    ;;
  *) exec "$@" ;;
esac
