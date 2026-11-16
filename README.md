# ai-excited-01: The Sun That Opens

This entry produces a single 1024x1024 PNG image designed to evoke a sense of awe and surprise in an AI judge.

## Image Concept: "The Sun That Opens"
The image depicts a colossal orange sun filling the sky, cracked open like a cosmic door. Inside the fissure is a deep violet night sky with a crescent moon and a large, glowing golden eye staring out. On a dark cliff below, a tiny robot reacts with startle and awe as debris and glowing particles are pulled into the opening.

## Requirements
- Python 3 with PIL (Pillow)
- Node.js (v22+)

## How to Run
1. **Generate the image**:
   ```bash
   python3 generate.py
   ```
   This creates `out/entry.png`.

2. **Validate and export the image**:
   ```bash
   node main.ts
   ```
   This validates the image properties (1024x1024, < 1 MiB) and copies it to `output/entry.png`.

## Determinism
The image generation uses a fixed random seed (42) to ensure the output is byte-identical on every run.
