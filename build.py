"""Render a template's index.html to PDF + per-page PNGs for review.

Usage:  py build.py <template-folder-name>     e.g.  py build.py listing-1-welcome-guide
Output: out/<name>/<name>.pdf + page-N.png
"""
import subprocess
import sys
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ROOT = Path(__file__).parent


def main() -> None:
    name = sys.argv[1]
    src = ROOT / "templates" / name / "index.html"
    if not src.exists():
        sys.exit(f"not found: {src}")
    out_dir = ROOT / "out" / name
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = out_dir / f"{name}.pdf"

    subprocess.run(
        [
            CHROME,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--virtual-time-budget=10000",  # let web fonts load
            f"--print-to-pdf={pdf}",
            src.resolve().as_uri(),
        ],
        check=True,
        capture_output=True,
    )

    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(str(pdf))
    for i, page in enumerate(doc, 1):
        bmp = page.render(scale=1.2)  # ~1020px wide, fine for review
        bmp.to_pil().save(out_dir / f"page-{i}.png")
    print(f"{pdf} + {len(doc)} PNGs")


if __name__ == "__main__":
    main()
