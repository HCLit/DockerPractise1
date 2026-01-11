# E-Learning Platform (scaffold)

This is a minimal scaffold for an e-learning platform that imports a PPTX as a course and serves lessons (one slide per lesson).

Quick usage

1. Build and run locally (optional Docker):

   ```bash
   cd elearning
   python -m venv .venv
   . .venv/bin/activate
   pip install -r requirements.txt
   python import_pptx.py --pptx ../e_learning_platform_architecture.pptx
   python app.py
   ```

2. Open http://localhost:5011 and view the imported course.

Notes
- The importer uses `pptx_viewer/convert.py` to create slide PNGs and `python-pptx` to extract notes. Ensure LibreOffice is available locally for conversion or use Docker.
