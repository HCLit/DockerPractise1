# PPTX Slide Viewer

A small Flask app that converts a PowerPoint `.pptx` into PNG slides (using LibreOffice) and serves a simple web viewer.

Features
- Converts `.pptx` -> PNG using LibreOffice (soffice)
- Simple web viewer with previous/next and keyboard navigation
- Dockerfile included for easy deployment

Quick start (local)

1. Install prerequisites (LibreOffice)

   macOS (Homebrew):
   ```
   brew install --cask libreoffice
   ```

2. Install Python deps:

   ```bash
   python -m venv .venv
   . .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Convert and run:

   ```bash
   python convert.py --pptx ../e_learning_platform_architecture.pptx --out slides
   python app.py
   ```

Open http://localhost:5000

Docker

Build and run:

```bash
docker build -t pptx-viewer .
docker run -p 5000:5000 -v $(pwd)/slides:/app/slides --env PPTX_FILE=/app/e_learning_platform_architecture.pptx pptx-viewer
```

Notes
- LibreOffice must be available in the runtime (the Dockerfile installs it).
- If your PPTX has embedded fonts or special content, LibreOffice's conversion may vary.
