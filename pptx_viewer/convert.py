#!/usr/bin/env python3
"""Convert a .pptx file to PNG slides using LibreOffice (soffice).

Usage:
    python convert.py --pptx path/to/file.pptx --out slides/

Requires: libreoffice (soffice) installed on the system or in the container.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_soffice():
    return shutil.which("soffice")


def convert_pptx_to_png(pptx_path: Path, out_dir: Path) -> None:
    if not pptx_path.exists():
        raise FileNotFoundError(f"PPTX not found: {pptx_path}")

    soffice = find_soffice()
    if not soffice:
        raise EnvironmentError("LibreOffice 'soffice' not found. Please install LibreOffice.")

    out_dir.mkdir(parents=True, exist_ok=True)

    # LibreOffice will produce PNGs into out_dir; use absolute paths
    cmd = [soffice, "--headless", "--invisible", "--convert-to", "png", "--outdir", str(out_dir), str(pptx_path)]
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pptx", required=True, help="Path to .pptx file")
    p.add_argument("--out", default="slides", help="Output directory for PNGs")
    args = p.parse_args()

    pptx = Path(args.pptx)
    out = Path(args.out)

    convert_pptx_to_png(pptx, out)
    print(f"Converted '{pptx}' -> '{out}'")


if __name__ == "__main__":
    main()
