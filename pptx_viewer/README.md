# PPTX Slide Viewer

[![CI](https://github.com/HCLit/DockerPractise1/actions/workflows/ci.yml/badge.svg)](https://github.com/HCLit/DockerPractise1/actions/workflows/ci.yml)

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

CI
- A GitHub Actions workflow (`.github/workflows/ci.yml`) runs unit tests on push and PRs. A separate job runs the optional Playwright E2E test on pushes (it installs Playwright browsers and runs the E2E test with `RUN_E2E=1`).

Publishing Docker images
- A workflow (`.github/workflows/publish-docker.yml`) builds and publishes Docker images to Docker Hub. It runs on pushes to `main|master|develop` branches and on tag pushes.
- Set the following repository secrets in GitHub (Repository -> Settings -> Secrets & variables -> Actions):
  - `DOCKERHUB_USERNAME` — your Docker Hub username
  - `DOCKERHUB_TOKEN` — Docker Hub password or access token (recommended when 2FA is enabled)

Tagging and pushes
- The workflow will push images to `$DOCKERHUB_USERNAME/pptx-viewer:latest` and also tag images with the commit sha and the git ref name (branch or tag). If you want images published only on semver tags, we can change the trigger/filter.

Running tests
- A small pytest integration suite is included: `tests/test_viewer_link.py`.
  - `test_open_reveal_link_present_and_script` validates the viewer HTML contains the Open Reveal link and the JS that sets its href.
  - An optional E2E test (`test_open_reveal_href_e2e`) uses Playwright to open `/`, waits for JavaScript to run, and checks the computed link (set `RUN_E2E=1` to enable this test). Example:

    ```bash
    # install test deps (Playwright needs browser binaries installed separately)
    pip install -r requirements.txt
    playwright install

    # unit-only tests:
    pytest -q

    # run E2E (headless) tests:
    RUN_E2E=1 pytest -q tests/test_viewer_link.py::test_open_reveal_href_e2e
    ```
