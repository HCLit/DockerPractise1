#!/usr/bin/env python3
"""Convert a .pptx file to numbered PNG slides.

Approach:
 - Use LibreOffice (`soffice`) to convert to PDF, then use `pdftoppm` (poppler) to render each PDF page to a PNG.
 - This reliably creates one PNG per slide named `slide_001.png`, `slide_002.png`, ...

Usage:
    python convert.py --pptx path/to/file.pptx --out slides --dpi 150

Requires: libreoffice (soffice) and pdftoppm (poppler-utils) installed.
"""

import argparse
import shutil
import subprocess
from pathlib import Path
import sys
import re

try:
    from pptx import Presentation
except Exception:
    Presentation = None


def find_exe(name):
    return shutil.which(name)


def count_slides(pptx_path: Path) -> int:
    if Presentation is None:
        return 0
    try:
        prs = Presentation(pptx_path)
        return len(prs.slides)
    except Exception:
        return 0


def clean_pngs(out_dir: Path):
    for p in out_dir.glob("*.png"):
        try:
            p.unlink()
        except Exception:
            pass


def pdf_to_png(pdf_path: Path, out_dir: Path, dpi: int = 150) -> None:
    pdftoppm = find_exe("pdftoppm")
    if not pdftoppm:
        raise EnvironmentError("pdftoppm not found. Install poppler/pdftoppm (e.g. 'brew install poppler' on macOS).")

    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = str(out_dir / "slide")
    cmd = [pdftoppm, "-png", f"-r", str(dpi), str(pdf_path), prefix]
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd)

    # pdftoppm outputs slide-1.png, slide-2.png; rename to slide_001.png etc.
    for p in out_dir.glob("slide-*.png"):
        m = re.search(r"slide-(\d+)\.png$", p.name)
        if m:
            idx = int(m.group(1))
            new_name = out_dir / f"slide_{idx:03d}.png"
            p.rename(new_name)


def convert_pptx_to_png(pptx_path: Path, out_dir: Path, dpi: int = 150, mode: str = "auto") -> None:
    if not pptx_path.exists():
        raise FileNotFoundError(f"PPTX not found: {pptx_path}")

    soffice = find_exe("soffice")
    if not soffice:
        raise EnvironmentError("LibreOffice 'soffice' not found. Please install LibreOffice.")

    out_dir.mkdir(parents=True, exist_ok=True)
    clean_pngs(out_dir)

    slide_count = count_slides(pptx_path) or 0
    print(f"Detected ~{slide_count} slides (0 if unknown)")

    use_pdf = (mode == "pdf") or (mode == "auto" and slide_count > 1)

    if use_pdf:
        # Convert to PDF first, then render each page
        pdf_path = out_dir / (pptx_path.stem + ".pdf")
        cmd = [soffice, "--headless", "--invisible", "--convert-to", "pdf", "--outdir", str(out_dir), str(pptx_path)]
        print("Converting to PDF with:", " ".join(cmd))
        subprocess.check_call(cmd)

        if not pdf_path.exists():
            # soffice might put the pdf in current dir; try to find any pdf with stem
            candidates = list(out_dir.glob(f"{pptx_path.stem}*.pdf"))
            if candidates:
                pdf_path = candidates[0]

        if not pdf_path.exists():
            raise RuntimeError("PDF conversion failed; PDF not found.")

        print(f"Rendering PDF -> PNG at {dpi} DPI")
        pdf_to_png(pdf_path, out_dir, dpi=dpi)

        # cleanup pdf
        try:
            pdf_path.unlink()
        except Exception:
            pass

    else:
        # Directly convert to PNG using soffice (may produce one image per slide depending on version)
        cmd = [soffice, "--headless", "--invisible", "--convert-to", "png", "--outdir", str(out_dir), str(pptx_path)]
        print("Running:", " ".join(cmd))
        subprocess.check_call(cmd)

        # Normalize names if soffice produced multiple similarly named files
        pngs = list(out_dir.glob("*.png"))
        if len(pngs) > 1:
            # Rename them deterministically
            for i, p in enumerate(sorted(pngs), start=1):
                new_name = out_dir / f"slide_{i:03d}.png"
                if p.name != new_name.name:
                    p.rename(new_name)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pptx", required=True, help="Path to .pptx file")
    p.add_argument("--out", default="slides", help="Output directory for PNGs")
    p.add_argument("--dpi", type=int, default=150, help="DPI for PDF rendering")
    p.add_argument("--mode", choices=["auto", "pdf", "soffice"], default="auto", help="Conversion mode")
    args = p.parse_args()

    pptx = Path(args.pptx)
    out = Path(args.out)

    convert_pptx_to_png(pptx, out, dpi=args.dpi, mode=args.mode)
    print(f"Converted '{pptx}' -> '{out}'")


if __name__ == "__main__":
    main()
