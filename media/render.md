# Re-render the explainer

1. Generate voice (needs `media/models/kokoro-v1.0.onnx` and `voices-v1.0.bin`):

```bash
uvx --from kokoro-onnx python media/tts.py
ffprobe -i media/narration.wav -show_entries format=duration -v quiet -of csv=p=0
```

2. Check and render:

```bash
cd media
npx --yes hyperframes@0.8.40 check
npx --yes hyperframes@0.8.40 render --quality high --output verse-cue.mp4
```
