"""Build one human-readable READOUT PDF from several markdown files.

Usage:
  python build-readout.py --out READOUT_x_v2.pdf --title "Project — v2" a.md b.md ...

Requires: `pip install markdown`, and Google Chrome or Microsoft Edge installed.
Each .md becomes a chapter (page break between), with a cover and a table of contents.
"""
import argparse
import datetime as dt
import os
import pathlib
import re
import subprocess
import sys
import tempfile

import markdown

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10.5pt; line-height: 1.4; color: #111; }
h1 { font-size: 18pt; margin: 0 0 6pt; }
h2 { font-size: 13.5pt; margin: 14pt 0 4pt; border-bottom: 1px solid #bbb; }
h3 { font-size: 11.5pt; margin: 10pt 0 3pt; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 6pt 0; }
th, td { border: 1px solid #999; padding: 3pt 5pt; vertical-align: top; }
th { background: #eee; } tr { page-break-inside: avoid; }
code { font-family: Consolas, monospace; font-size: 9pt; background: #f2f2f2; padding: 0 2pt; }
blockquote { border-left: 3px solid #c90; margin: 6pt 0; padding: 2pt 8pt; background: #fff8e6; }
hr { border: 0; border-top: 1px solid #bbb; margin: 10pt 0; }
.chapter { page-break-before: always; }
.cover { height: 90vh; display: flex; flex-direction: column; justify-content: center; }
.cover h1 { font-size: 30pt; } .cover p { font-size: 13pt; color: #444; }
.toc ol { font-size: 12pt; line-height: 1.8; }
"""


def find_chrome():
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    sys.exit("Chrome/Edge not found; install one or edit CHROME_CANDIDATES")


def first_heading(md_text, fallback):
    m = re.search(r"^#\s+(.+)$", md_text, re.M)
    return m.group(1).strip() if m else fallback


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("files", nargs="+")
    a = ap.parse_args()

    chapters = []
    for f in a.files:
        p = pathlib.Path(f)
        text = p.read_text(encoding="utf-8")
        chapters.append((first_heading(text, p.stem), text))

    toc = "".join(f"<li>{t}</li>" for t, _ in chapters)
    body = [
        f"<div class='cover'><h1>{a.title}</h1><p>{a.subtitle}</p>"
        f"<p>{dt.date.today().isoformat()}</p></div>",
        f"<div class='chapter toc'><h1>Содержание</h1><ol>{toc}</ol></div>",
    ]
    for _, text in chapters:
        html = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
        body.append(f"<div class='chapter'>{html}</div>")

    doc = ("<!doctype html><html><head><meta charset='utf-8'>"
           f"<style>{CSS}</style></head><body>{''.join(body)}</body></html>")

    out = pathlib.Path(a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8",
                                     dir=str(out.parent)) as tmp:
        tmp.write(doc)
        tmp_path = pathlib.Path(tmp.name)
    try:
        subprocess.run([find_chrome(), "--headless=new", "--disable-gpu",
                        "--no-pdf-header-footer", f"--print-to-pdf={out}", tmp_path.as_uri()],
                       check=True, capture_output=True)
    finally:
        tmp_path.unlink(missing_ok=True)
    print(out, out.stat().st_size)


if __name__ == "__main__":
    main()
