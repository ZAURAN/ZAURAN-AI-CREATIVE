#!/usr/bin/env python3
"""Read the private book library. Standard library only; no writes or network.

Offsets are zero-based Unicode character offsets into the selected text, index,
catalog, or deterministic search listing. PDF page numbers are physical pages.
"""
import argparse
import bisect
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET


LIBRARY = pathlib.Path(__file__).resolve().parents[1] / "library" / "books"
BOOK_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
PAGE = re.compile(r"^\[\[PDF_PAGE_(\d{3,})\]\]$", re.MULTILINE)


class ReaderError(Exception):
    """An actionable library or argument error, without a Python traceback."""


def local_path(root, name):
    resolved = (root / name).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ReaderError("Library path escapes its directory.")
    return resolved


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as error:
        raise ReaderError(f"Local library file unavailable: {path}") from error
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ReaderError(f"Invalid UTF-8 JSON file: {path}") from error


def load_catalog():
    catalog = read_json(local_path(LIBRARY, "catalog.json"))
    if not isinstance(catalog, list):
        raise ReaderError("Catalog must contain a JSON array of book records.")
    ids = []
    for book in catalog:
        if not isinstance(book, dict) or not isinstance(book.get("id"), str):
            raise ReaderError("Catalog record is missing a valid book ID.")
        if not BOOK_ID.fullmatch(book["id"]) or book["id"] in ids:
            raise ReaderError("Catalog contains an unsafe or duplicate book ID.")
        ids.append(book["id"])
    return catalog


def load_index(folder):
    index = read_json(local_path(folder, "index.json"))
    if not isinstance(index, list):
        raise ReaderError("Book index must contain a JSON array.")
    previous, ids = 0, set()
    for entry in index:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            raise ReaderError("Book index contains an invalid section record.")
        line = entry.get("line")
        if type(line) is not int or line <= previous or entry["id"] in ids:
            raise ReaderError("Book index has duplicate IDs or invalid line positions.")
        path = entry.get("path", [])
        if not isinstance(path, list) or not all(isinstance(p, str) for p in path):
            raise ReaderError("Book index has an invalid title path.")
        if not isinstance(entry.get("title", ""), str):
            raise ReaderError("Book index has an invalid title.")
        previous = line
        ids.add(entry["id"])
    return index


def xml_depths(folder, index):
    """Old title-path indexes lose unnamed-node depth; recover it from FB2."""
    source = local_path(folder, "source.fb2")
    if not source.exists():
        return None
    try:
        root = ET.parse(source).getroot()
    except ET.ParseError as error:
        raise ReaderError("source.fb2 is not valid XML; cannot verify section hierarchy.") from error
    found = []
    stack = [(root, 0)]
    while stack:
        element, depth = stack.pop()
        section = element.tag.rsplit("}", 1)[-1] == "section"
        if section:
            title = next((c for c in element if c.tag.rsplit("}", 1)[-1] == "title"), None)
            words = "" if title is None else "".join(title.itertext())
            found.append((depth, "".join(words.split())))
        stack.extend((child, depth + int(section)) for child in reversed(element))
    titles = ["".join(row.get("title", "").split()) for row in index]
    if len(found) != len(index) or [title for _, title in found] != titles:
        raise ReaderError("source.fb2 and index.json disagree; re-import before reading sections.")
    return [depth for depth, _ in found]


def path_descendant(parent, candidate):
    path, other = parent.get("path", []), candidate.get("path", [])
    if len(other) > len(path) and other[:len(path)] == path:
        return True
    return bool(parent.get("title")) and not candidate.get("title") and other == path


def hierarchy_depths(folder, index):
    depths = xml_depths(folder, index)
    if depths is not None or not all("parent_id" in row for row in index):
        return depths
    known = {}
    for row in index:
        parent = row["parent_id"]
        if parent is not None and (not isinstance(parent, str) or parent not in known):
            raise ReaderError("Book index has an invalid parent_id hierarchy.")
        known[row["id"]] = 0 if parent is None else known[parent] + 1
    return [known[row["id"]] for row in index]


def section_text(folder, index, text, section_id):
    position = next((i for i, row in enumerate(index) if row["id"] == section_id), None)
    if position is None:
        raise ReaderError(f"Unknown section {section_id!r}; use --index for valid IDs.")
    lines = text.split("\n")
    line_count = len(lines) - int(text.endswith("\n")) if text else 0
    if index and index[-1]["line"] > line_count:
        raise ReaderError("Book index points beyond the end of text.txt.")
    depths = hierarchy_depths(folder, index)
    row = index[position]
    if depths is None and not row.get("title"):
        raise ReaderError(
            "Unnamed section hierarchy is ambiguous in a legacy title-path index. "
            "Restore source.fb2 or an index with exact parent_id values; "
            "depth and subtree_end_line hints alone cannot verify this selection."
        )
    end = line_count
    for i in range(position + 1, len(index)):
        descendant = (depths[i] > depths[position] if depths is not None
                      else path_descendant(row, index[i]))
        if not descendant:
            end = index[i]["line"] - 1
            break
    content = "\n".join(lines[row["line"] - 1:end]) + ("\n" if end < len(lines) else "")
    return content, f"{section_id}; lines {row['line']}–{end}"


def page_text(book, text, page):
    if book.get("source_file") != "source.pdf":
        raise ReaderError("--page requires a PDF book; use --section for FB2.")
    markers = list(PAGE.finditer(text))
    positions = [i for i, match in enumerate(markers) if int(match[1]) == page]
    if len(positions) != 1:
        raise ReaderError(f"Physical PDF page {page} has no unique standalone marker.")
    i = positions[0]
    end = markers[i + 1].start() if i + 1 < len(markers) else len(text)
    return text[markers[i].start():end], f"physical PDF page {page}"


def search_hits(text, query):
    """Yield bounded context per occurrence, retaining original Unicode spelling."""
    needle = query.casefold()
    starts = [0] + [match.end() for match in re.finditer("\n", text)]
    for line_number, line in enumerate(text.split("\n"), 1):
        folded = line.casefold()
        if needle not in folded:
            continue
        offsets = [0]
        for char in line:
            offsets.append(offsets[-1] + len(char.casefold()))
        position = folded.find(needle)
        while position >= 0:
            first = bisect.bisect_right(offsets, position) - 1
            last = bisect.bisect_left(offsets, position + len(needle))
            left, right = max(0, first - 90), min(len(line), last + 90)
            excerpt = ("…" if left else "") + line[left:right] + ("…" if right < len(line) else "")
            yield f"line {line_number}; char {starts[line_number - 1] + first}: {excerpt}\n"
            position = folded.find(needle, position + len(needle))


def window(chunks, offset, maximum):
    """Scan a stream, retaining only the requested character window in memory."""
    total, count, selected = 0, 0, []
    for chunk in chunks:
        left, right = max(0, offset - total), min(len(chunk), offset + maximum - total)
        if left < right:
            selected.append(chunk[left:right])
        total += len(chunk)
        count += 1
    if offset > total:
        raise ReaderError(f"--offset {offset} exceeds selected text length {total}.")
    return "".join(selected), total, count


def arguments(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list", action="store_true", help="List available catalog books")
    mode.add_argument("--index", action="store_true", help="Show the selected book's JSON index")
    mode.add_argument("--section", help="Read an indexed section including descendants")
    mode.add_argument("--page", type=int, help="Read a physical PDF page")
    mode.add_argument("--query", help="Case-insensitive literal search within individual lines")
    parser.add_argument("--book", help="Book ID from --list (never a filesystem path)")
    parser.add_argument("--offset", type=int, default=0, help="Character offset into selected output")
    parser.add_argument("--max-chars", type=int, default=12000, help="Output window (1–100000 characters)")
    args = parser.parse_args(argv)
    if args.list == bool(args.book):
        parser.error("Use --list alone, or --book ID with --index/--section/--page/--query.")
    if args.offset < 0 or not 1 <= args.max_chars <= 100000:
        parser.error("--offset must be nonnegative and --max-chars must be between 1 and 100000.")
    if args.page is not None and args.page < 1:
        parser.error("--page must be a positive physical page number.")
    if args.query is not None and (not args.query.strip() or len(args.query) > 512 or "\n" in args.query or "\r" in args.query):
        parser.error("--query must contain 1–512 characters on a single nonempty line.")
    return args


def select(args, catalog):
    if args.list:
        rows = [f"{b['id']} | {b.get('author', '')} | {b.get('title', '')}\n{b.get('coverage', '')}\n" for b in catalog]
        return rows or ["Library catalog is empty.\n"], "Local book catalog"
    book = next((b for b in catalog if b["id"] == args.book), None)
    if book is None:
        raise ReaderError(f"Unknown book ID {args.book!r}; use --list for available IDs.")
    folder = local_path(LIBRARY, book["id"])
    heading = f"{book['id']} | {book.get('title', '')}\nCoverage: {book.get('coverage', 'unspecified')}"
    if args.index:
        return [json.dumps(load_index(folder), ensure_ascii=False, indent=2)], heading + "\nIndex"
    text = local_path(folder, "text.txt").read_text(encoding="utf-8-sig")
    if args.query is not None:
        return search_hits(text, args.query), heading + f"\nSearch: {args.query!r}"
    if args.page is not None:
        content, locator = page_text(book, text, args.page)
    else:
        content, locator = section_text(folder, load_index(folder), text, args.section)
    return [content], heading + "\n" + locator


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    args = arguments(argv)
    try:
        chunks, heading = select(args, load_catalog())
        excerpt, total, count = window(chunks, args.offset, args.max_chars)
        print(heading)
        if args.query is not None:
            print(f"{count} hits; each excerpt has up to 90 characters of context per side.")
        end = min(total, args.offset + args.max_chars)
        print(f"Characters [{args.offset}:{end}] of {total}; zero-based, end exclusive.\n")
        print(excerpt)
        if end < total:
            print(f"\n[TRUNCATED: repeat the same selection with --offset {end} --max-chars {args.max_chars}]")
        else:
            print("\n[END OF SELECTION]")
        return 0
    except (ReaderError, OSError, UnicodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
