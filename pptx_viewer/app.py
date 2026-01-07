import os
from flask import Flask, render_template, send_from_directory, url_for
from pathlib import Path
import subprocess

app = Flask(__name__)
BASE_DIR = Path(__file__).parent
SLIDES_DIR = BASE_DIR / "slides"
PPTX_FILE = os.environ.get("PPTX_FILE", str(BASE_DIR.parent / "e_learning_platform_architecture.pptx"))


def ensure_slides():
    # If slides folder is empty, try to convert
    slides = sorted(SLIDES_DIR.glob("*.png"))
    if slides:
        return

    # Attempt conversion using convert.py
    convert_script = BASE_DIR / "convert.py"
    cmd = ["python", str(convert_script), "--pptx", PPTX_FILE, "--out", str(SLIDES_DIR)]
    print("Converting PPTX -> PNG using:", cmd)
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print("Conversion failed:", e)


@app.route("/")
def index():
    ensure_slides()
    images = sorted([p.name for p in SLIDES_DIR.glob("*.png")])
    return render_template("index.html", images=images)


@app.route("/slides/<path:filename>")
def slides(filename):
    return send_from_directory(SLIDES_DIR, filename)


if __name__ == "__main__":
    # ensure folder exists
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
