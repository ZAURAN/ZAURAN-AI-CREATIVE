"""Build one human-readable READOUT PDF from several markdown files.

Usage:
  python build-readout.py --out READOUT_x_v2.pdf --title "Project — v2" a.md b.md ...

Requires: `pip install markdown`, and Google Chrome or Microsoft Edge installed.
Each .md becomes a chapter (page break between), with a cover and a table of contents.
Existing PDFs are never overwritten: choose a new versioned output name.
HTML is sanitized; images become alt text and scripts/resources are disabled.
Publication uses an atomic hard link when supported; otherwise exclusive copy
prevents overwrite, but readers may see a partial file until copying finishes.
"""
import argparse
import datetime as dt
import errno
from html import escape
from html.parser import HTMLParser
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit

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


class BuildError(Exception):
    """An actionable readout build failure."""


def find_chrome(explicit=None):
    if explicit:
        path = pathlib.Path(explicit).expanduser()
        executable = str(path.resolve()) if path.is_file() else shutil.which(explicit)
        if executable:
            return executable
        raise BuildError(f"Browser not found: {explicit}")
    for p in CHROME_CANDIDATES:
        if pathlib.Path(p).is_file():
            return p
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge"):
        if executable := shutil.which(name):
            return executable
    raise BuildError("Chrome/Edge not found; install one or pass --browser PATH")


class ReadoutHTML(HTMLParser):
    """Keep Markdown formatting while dropping all executable/resource attributes."""

    TAGS = frozenset(('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li',
                      'em', 'strong', 'blockquote', 'pre', 'code', 'hr', 'br', 'a',
                      'table', 'thead', 'tbody', 'tr', 'th', 'td', 'del', 's', 'sup', 'sub'))
    VOID = frozenset(('hr', 'br'))

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'img':
            self.parts.append(escape(values.get('alt') or '[image omitted]'))
            return
        if tag not in self.TAGS:
            # Preserve unsupported markup as visible, inert text.
            self.parts.append(escape('<' + tag + '>'))
            return
        attributes = ''
        href = (values.get('href') or '').strip()
        if tag == 'a' and self.safe_link(href):
            attributes = f' href="{escape(href, quote=True)}" rel="noreferrer noopener"'
        self.parts.append(f'<{tag}{attributes}>')

    @staticmethod
    def safe_link(href):
        if not href or any(ord(char) < 32 for char in href):
            return False
        try:
            return href.startswith('#') or urlsplit(href).scheme.lower() in ('https', 'http', 'mailto')
        except ValueError:
            return False

    def handle_endtag(self, tag):
        if tag in self.TAGS and tag not in self.VOID:
            self.parts.append(f'</{tag}>')
        elif tag not in self.TAGS and tag != 'img':
            self.parts.append(escape(f'</{tag}>'))

    def handle_data(self, data):
        self.parts.append(escape(data))


def safe_markdown(source):
    parser = ReadoutHTML()
    parser.feed(markdown.markdown(source, extensions=['tables', 'fenced_code', 'sane_lists']))
    parser.close()
    return ''.join(parser.parts)


def first_heading(md_text, fallback):
    m = re.search(r"^#\s+(.+)$", md_text, re.M)
    return m.group(1).strip() if m else fallback


def build_document(title, subtitle, chapters):
    toc = "".join(f"<li>{escape(t)}</li>" for t, _ in chapters)
    body = [
        f"<div class='cover'><h1>{escape(title)}</h1><p>{escape(subtitle)}</p>"
        f"<p>{dt.date.today().isoformat()}</p></div>",
        f"<div class='chapter toc'><h1>Содержание</h1><ol>{toc}</ol></div>",
    ]
    for _, text in chapters:
        body.append(f"<div class='chapter'>{safe_markdown(text)}</div>")

    return ("<!doctype html><html><head><meta charset='utf-8'>"
            '<meta http-equiv="Content-Security-Policy" '
            'content="default-src \'none\'; style-src \'unsafe-inline\'; '
            'base-uri \'none\'; form-action \'none\'">'
            f"<style>{CSS}</style></head><body>{''.join(body)}</body></html>")


def render_pdf(doc, out, browser, timeout=60):
    out = pathlib.Path(out).absolute()
    if os.path.lexists(out):
        raise BuildError(f"Output already exists; choose a new version: {out}")
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.readout-', dir=out.parent) as temp:
        root = pathlib.Path(temp)
        html_path, pdf_path = root / 'readout.html', root / 'rendered.pdf'
        html_path.write_text(doc, encoding='utf-8')
        run_browser(browser, html_path, pdf_path, root / 'profile', timeout)
        if not pdf_path.is_file() or pdf_path.stat().st_size <= 5:
            raise BuildError('Browser did not produce a nonempty PDF')
        with pdf_path.open('rb') as pdf:
            if pdf.read(5) != b'%PDF-':
                raise BuildError('Browser produced an invalid PDF header')
        try:
            # Same-volume hard link atomically publishes without replacing another writer.
            os.link(pdf_path, out)
        except FileExistsError as exc:
            raise BuildError(f'Output already exists; choose a new version: {out}') from exc
        except OSError as exc:
            unsupported = exc.errno in (errno.ENOTSUP, errno.EOPNOTSUPP, errno.ENOSYS,
                                        errno.EXDEV, errno.EPERM)
            if unsupported or getattr(exc, 'winerror', None) in (1, 17, 50):
                exclusive_copy(pdf_path, out)
            else:
                raise BuildError(f'Cannot publish PDF: {exc}') from exc
    return out


def exclusive_copy(source, out):
    """Fallback without overwrite; copy visibility is not atomic on these filesystems."""
    try:
        target = out.open('xb')
    except FileExistsError as exc:
        raise BuildError(f'Output already exists; choose a new version: {out}') from exc
    except OSError as exc:
        raise BuildError(f'Cannot create PDF output: {exc}') from exc
    identity = None
    try:
        with target:
            identity = os.fstat(target.fileno())
            with source.open('rb') as pdf:
                shutil.copyfileobj(pdf, target)
            target.flush()
            os.fsync(target.fileno())
    except OSError as exc:
        try:
            # Never clean up a replacement created by another writer after our copy.
            if identity is not None and os.path.samestat(identity, out.stat(follow_symlinks=False)):
                out.unlink()
        except FileNotFoundError:
            pass
        except OSError as cleanup_error:
            raise BuildError(f'Cannot copy PDF: {exc}; partial output cleanup failed: '
                             f'{cleanup_error}') from exc
        raise BuildError(f'Cannot copy PDF: {exc}') from exc


def run_browser(browser, html_path, pdf_path, profile, timeout):
    try:
        subprocess.run([browser, '--headless=new', '--disable-gpu', '--disable-extensions',
                        '--disable-background-networking', '--no-first-run',
                        f'--user-data-dir={profile}', '--no-pdf-header-footer',
                        f'--print-to-pdf={pdf_path}', html_path.as_uri()],
                       check=True, capture_output=True, text=True, errors='replace',
                       timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise BuildError(f'Browser timed out after {timeout:g} seconds; adjust --timeout') from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or '').strip()[-500:]
        raise BuildError(f'Browser failed with exit code {exc.returncode}: {detail}') from exc
    except OSError as exc:
        raise BuildError(f'Cannot start browser: {exc}') from exc


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True)
    ap.add_argument('--title', required=True)
    ap.add_argument('--subtitle', default='')
    ap.add_argument('--browser', help='Chrome/Edge executable path or PATH command')
    ap.add_argument('--timeout', type=int, default=60, help='Browser timeout in seconds (default: 60)')
    ap.add_argument('files', nargs='+')
    args = ap.parse_args(argv)
    if args.timeout <= 0:
        ap.error('--timeout must be a positive number of seconds')
    try:
        chapters = []
        for name in args.files:
            path = pathlib.Path(name)
            source = path.read_text(encoding='utf-8-sig')
            chapters.append((first_heading(source, path.stem), source))
        doc = build_document(args.title, args.subtitle, chapters)
        out = render_pdf(doc, args.out, find_chrome(args.browser), args.timeout)
    except (BuildError, OSError, UnicodeError) as exc:
        print(f'Readout build failed: {exc}', file=sys.stderr)
        return 1
    print(out, out.stat().st_size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
