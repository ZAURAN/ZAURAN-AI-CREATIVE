"""Read-only local reader regression tests using an isolated miniature library."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "read-book.py"


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.script = self.root / "skill" / "scripts" / "read-book.py"
        self.script.parent.mkdir(parents=True)
        if SCRIPT.exists():
            shutil.copyfile(SCRIPT, self.script)
        self.books = self.root / "skill" / "library" / "books"
        self.books.mkdir(parents=True)
        self.catalog = [
            {"id": "drama", "title": "Драма", "source_file": "source.fb2", "coverage": "fragment"},
            {"id": "pdf", "title": "PDF", "source_file": "source.pdf"},
        ]
        self.write_json(self.books / "catalog.json", self.catalog)
        self.drama = self.books / "drama"
        self.drama.mkdir()
        self.lines = ["preamble", "PARENT", "parent body", "CHILD", "child body",
                      "GRANDCHILD", "grandchild body", "SIBLING", "sibling body",
                      "FINAL", "Конфликт Straße КОНФЛИКТ", "final body"]
        (self.drama / "text.txt").write_text("\n".join(self.lines), encoding="utf-8")
        self.index = [
            {"id": "S001", "title": "PARENT", "path": ["PARENT"], "line": 2, "end_line": 3},
            {"id": "S002", "title": "CHILD", "path": ["PARENT", "CHILD"], "line": 4, "end_line": 5},
            {"id": "S003", "title": "GRANDCHILD", "path": ["PARENT", "CHILD", "GRANDCHILD"], "line": 6, "end_line": 7},
            {"id": "S004", "title": "SIBLING", "path": ["SIBLING"], "line": 8, "end_line": 9},
            {"id": "S005", "title": "FINAL", "path": ["FINAL"], "line": 10, "end_line": 12},
        ]
        self.write_json(self.drama / "index.json", self.index)
        pdf = self.books / "pdf"
        pdf.mkdir()
        (pdf / "text.txt").write_text(
            "[[PDF_PAGE_001]]\nFirst\nMention PDF_PAGE_002 in prose.\n"
            "[[PDF_PAGE_002]]\nSecond\n[[PDF_PAGE_003]]\nLast", encoding="utf-8")
        self.write_json(pdf / "index.json", [{"id": "PDF_PAGE_001", "title": "Chapter", "line": 1, "end_line": 7}])

    @staticmethod
    def write_json(path, value):
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def run_reader(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(self.script), *args], cwd=self.root,
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode == 0, ok, result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        return result

    def test_list_index_and_arbitrary_working_directory(self):
        result = self.run_reader("--list")
        self.assertIn("Драма", result.stdout)
        self.assertIn("fragment", result.stdout)
        self.assertIn("S003", self.run_reader("--book", "drama", "--index").stdout)

    def test_nested_subtree_excludes_next_sibling(self):
        result = self.run_reader("--book", "drama", "--section", "S001")
        self.assertIn("grandchild body", result.stdout)
        self.assertNotIn("sibling body", result.stdout)
        child = self.run_reader("--book", "drama", "--section", "S002").stdout
        self.assertIn("grandchild body", child)
        self.assertNotIn("parent body", child)

    def test_final_section_reaches_end_of_text(self):
        self.assertIn("final body", self.run_reader("--book", "drama", "--section", "S005").stdout)

    def test_unnamed_child_with_same_title_path_is_included(self):
        changed = [dict(row) for row in self.index]
        changed[1].update(title="", path=["PARENT"], depth=1)
        changed[0].update(subtree_end_line=3)
        self.write_json(self.drama / "index.json", changed)
        result = self.run_reader("--book", "drama", "--section", "S001")
        self.assertIn("grandchild body", result.stdout)
        self.assertNotIn("sibling body", result.stdout)

    def test_xml_hierarchy_resolves_unnamed_sibling_ambiguity(self):
        # Empty paths cannot distinguish root siblings from nested unnamed sections.
        changed = [dict(row, title="", path=[], depth=0) for row in self.index]
        self.write_json(self.drama / "index.json", changed)
        (self.drama / "source.fb2").write_text(
            '<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0"><body>'
            '<section><section><section/></section></section><section/><section/>'
            '</body></FictionBook>', encoding="utf-8")
        result = self.run_reader("--book", "drama", "--section", "S001")
        self.assertIn("grandchild body", result.stdout)
        self.assertNotIn("sibling body", result.stdout)

    def test_parent_ids_preserve_unnamed_hierarchy_without_source_xml(self):
        parents = [None, "S001", "S002", None, None]
        changed = [dict(row, title="", path=[], parent_id=parent)
                   for row, parent in zip(self.index, parents)]
        self.write_json(self.drama / "index.json", changed)
        result = self.run_reader("--book", "drama", "--section", "S001")
        self.assertIn("grandchild body", result.stdout)
        self.assertNotIn("sibling body", result.stdout)

    def test_legacy_unnamed_root_does_not_trust_depth_or_subtree_hints(self):
        changed = [dict(row, title="", path=[], depth=depth, subtree_end_line=7)
                   for row, depth in zip(self.index, [0, 1, 2, 0, 0])]
        self.write_json(self.drama / "index.json", changed)
        result = self.run_reader("--book", "drama", "--section", "S001", ok=False)
        self.assertIn("source.fb2", result.stderr)
        self.assertIn("parent_id", result.stderr)
        self.assertNotIn("parent body", result.stdout)

    def test_legacy_unnamed_child_with_same_path_descendant_is_rejected(self):
        changed = [dict(row) for row in self.index]
        changed[1].update(title="", path=["PARENT"], depth=2, subtree_end_line=7)
        changed[2].update(title="", path=["PARENT"], depth=3, subtree_end_line=7)
        self.write_json(self.drama / "index.json", changed)
        result = self.run_reader("--book", "drama", "--section", "S002", ok=False)
        self.assertIn("source.fb2", result.stderr)
        self.assertIn("parent_id", result.stderr)
        self.assertNotIn("child body", result.stdout)
        # Its titled ancestor still has an unambiguous boundary at the next title path.
        titled = self.run_reader("--book", "drama", "--section", "S001")
        self.assertIn("grandchild body", titled.stdout)
        self.assertNotIn("sibling body", titled.stdout)

    def test_physical_lines_are_newlines_not_unicode_separators(self):
        changed = [line.replace("child body", "child\u2028body") for line in self.lines]
        (self.drama / "text.txt").write_text("\n".join(changed), encoding="utf-8")
        result = self.run_reader("--book", "drama", "--section", "S005")
        self.assertNotIn("sibling body", result.stdout)
        self.assertIn("line 11", self.run_reader("--book", "drama", "--query", "STRASSE").stdout)

    def test_xml_and_index_mismatch_fails_without_guessing(self):
        (self.drama / "source.fb2").write_text("<FictionBook><body/></FictionBook>", encoding="utf-8")
        result = self.run_reader("--book", "drama", "--section", "S001", ok=False)
        self.assertIn("disagree", result.stderr)

    def test_pdf_physical_page_requires_exact_standalone_marker(self):
        result = self.run_reader("--book", "pdf", "--page", "2")
        self.assertIn("Second", result.stdout)
        self.assertNotIn("prose", result.stdout)
        self.assertNotIn("Last", result.stdout)
        self.assertIn("Last", self.run_reader("--book", "pdf", "--page", "3").stdout)
        self.run_reader("--book", "pdf", "--page", "4", ok=False)
        self.run_reader("--book", "drama", "--page", "1", ok=False)

    def test_search_is_casefolded_and_bounded_with_line_locators(self):
        result = self.run_reader("--book", "drama", "--query", "STRASSE")
        self.assertIn("Straße", result.stdout)
        self.assertIn("line 11", result.stdout)
        matches = self.run_reader("--book", "drama", "--query", "конфликт").stdout
        self.assertIn("2 hits", matches)
        bounded = self.run_reader("--book", "drama", "--query", "a", "--max-chars", "40")
        self.assertIn("TRUNCATED", bounded.stdout)
        self.assertLess(len(bounded.stdout), 700)
        self.assertIn("0 hits", self.run_reader("--book", "drama", "--query", "missing").stdout)

    def test_offset_and_truncation_have_precise_continuation(self):
        result = self.run_reader("--book", "drama", "--section", "S001", "--max-chars", "6")
        self.assertIn("\nPARENT\n", result.stdout)
        self.assertIn("--offset 6", result.stdout)
        result = self.run_reader("--book", "drama", "--section", "S001", "--offset", "7", "--max-chars", "11")
        self.assertIn("\nparent body\n", result.stdout)
        self.assertIn("--offset 18", result.stdout)
        self.run_reader("--book", "drama", "--section", "S001", "--offset", "999", ok=False)

    def test_invalid_ids_and_arguments_fail_without_traceback(self):
        for args in [
            ("--book", "../drama", "--index"), ("--book", "unknown", "--index"),
            ("--book", "drama", "--section", "S999"), ("--index",),
            ("--list", "--book", "drama"), ("--book", "drama"),
            ("--book", "drama", "--query", ""), ("--book", "pdf", "--page", "0"),
            ("--list", "--offset", "-1"), ("--list", "--max-chars", "0"),
        ]:
            with self.subTest(args=args):
                self.run_reader(*args, ok=False)

    def test_catalog_cannot_authorize_path_traversal(self):
        self.write_json(self.books / "catalog.json", [{"id": "../escape", "title": "bad"}])
        self.run_reader("--book", "../escape", "--index", ok=False)

    def test_missing_and_empty_libraries(self):
        self.write_json(self.books / "catalog.json", [])
        self.assertIn("empty", self.run_reader("--list").stdout.lower())
        self.run_reader("--book", "drama", "--index", ok=False)
        (self.books / "catalog.json").unlink()
        self.run_reader("--list", ok=False)

    def test_corrupt_catalog_and_index_fail_cleanly(self):
        self.write_json(self.drama / "index.json", [{"id": "S001", "line": -1}])
        self.run_reader("--book", "drama", "--section", "S001", ok=False)
        (self.books / "catalog.json").write_text("not JSON", encoding="utf-8")
        self.run_reader("--list", ok=False)


if __name__ == "__main__":
    unittest.main()
