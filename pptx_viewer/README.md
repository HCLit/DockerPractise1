# PPTX Slide Viewer

A small Flask app that converts a PowerPoint `.pptx` into PNG slides (using LibreOffice) and serves a simple web viewer.

Features
- Converts `.pptx` -> PNG using LibreOffice (soffice)
- Simple web viewer with previous/next and keyboard navigation
- Dockerfile included for easy deployment

Quick start (local)

1. Install prerequisites (LibreOffice and Poppler)

   macOS (Homebrew):
   ```
   brew install --cask libreoffice
   brew install poppler    # provides pdftoppm used for multi-slide PNG output
   ```

   Note: the converter now produces one PNG per slide (named `slide_001.png`, `slide_002.png`, ...). If you're using Docker, poppler is already included in the image.

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

Notes & Assets
- The app now extracts speaker notes and slide assets. Visit `http://<host>:<port>/notes` to browse notes and download embedded images.
- Extracted assets are stored under `slides/assets/` and a `slides/notes.json` file lists the notes and asset filenames.

Reveal.js deck
- You can view the slides as a Reveal.js presentation (with speaker notes) at `http://<host>:<port>/reveal`.
- In Reveal, press `s` to open the speaker notes window (or append `?presenter=true`).
- The Reveal page now includes a thumbnail strip (bottom) for quick navigation and a small custom theme for cleaner visuals. Click any thumbnail to jump to that slide or use the keyboard (← →) to navigate.
- Thumbnails can be toggled on/off with the **Toggle Thumbnails** button. The initial visibility can also be set with the `thumbs` query parameter (e.g. `/reveal?thumbs=false`). The user's preference is persisted in browser localStorage.
- The main viewer (`/`) now has an **Open Reveal** button that opens the deck with your current thumbnail preference (reads localStorage and includes `?thumbs=true|false` in the URL). This makes it easy to share or reopen the deck with the same thumbnail state.
