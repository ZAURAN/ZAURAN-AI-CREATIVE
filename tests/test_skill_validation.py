"""Validate canonical and legacy workflows through the actual CLI."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_skills.py'


class SkillValidationTests(unittest.TestCase):
    def run_check(self, extra_path, text):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            script = root / 'scripts/check_skills.py'
            script.parent.mkdir()
            script.write_bytes(SCRIPT.read_bytes())
            (root / 'SKILL.md').write_text('---\nname: zauran-ai-creative\ndescription: "Root"\n---\n', encoding='utf-8')
            extra = root / extra_path
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text(text, encoding='utf-8')
            return subprocess.run([sys.executable, str(script)], text=True, capture_output=True, encoding='utf-8')

    def test_valid_canonical_skill_is_counted(self):
        result = self.run_check('skills/zauran-new/SKILL.md', '---\nname: zauran-new\ndescription: "New"\n---\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('2 skills OK', result.stdout)

    def test_invalid_canonical_skill_fails(self):
        result = self.run_check('skills/zauran-new/SKILL.md', '---\nname: wrong\ndescription: "New"\n---\n')
        self.assertEqual(result.returncode, 1)
        self.assertIn('name must be zauran-new', result.stdout)

    def test_legacy_nested_skill_still_validates(self):
        result = self.run_check('zauran-old/SKILL.md', '---\nname: zauran-old\ndescription: "Old"\n---\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('2 skills OK', result.stdout)

    def test_canonical_json_failure_is_reported(self):
        result = self.run_check('skills/zauran-new/references/data.json', '{broken')
        self.assertEqual(result.returncode, 1)
        self.assertIn('data.json', result.stdout)


if __name__ == '__main__':
    unittest.main()
