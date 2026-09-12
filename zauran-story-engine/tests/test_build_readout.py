"""Security and publication regressions; no browser needed for unit tests."""
import importlib.util
import contextlib
import io
import errno
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock


SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "build-readout.py"
SPEC = importlib.util.spec_from_file_location("build_readout", SCRIPT)
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class HtmlTests(unittest.TestCase):
    def test_headings_and_safe_link_boundaries(self):
        self.assertEqual(builder.first_heading('text\n# Chapter\nmore', 'fallback'), 'Chapter')
        self.assertEqual(builder.first_heading('no heading', 'fallback'), 'fallback')
        for href in ('', 'java\nscript:alert(1)', 'https://[broken', '/secret', '//remote'):
            with self.subTest(href=href):
                self.assertFalse(builder.ReadoutHTML.safe_link(href))
        self.assertTrue(builder.ReadoutHTML.safe_link('#chapter'))
        self.assertTrue(builder.ReadoutHTML.safe_link('mailto:a@example.com'))

    def test_cover_and_toc_escape_plain_text(self):
        doc = builder.build_document('<script>alert(1)</script>', '<img src=x>',
                                     [('<iframe src=x>', '# Safe')])
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', doc)
        self.assertIn('&lt;img src=x&gt;', doc)
        self.assertIn('&lt;iframe src=x&gt;', doc)
        self.assertNotIn('<script', doc)
        self.assertNotIn('<img', doc)

    def test_markdown_preserves_tables_and_blocks_active_resources(self):
        source = '''# Heading

| Name | Value |
| --- | --- |
| A | B |

<script>alert(1)</script>
<style>@import url(https://bad.example/x);</style>
<iframe src="file:///secret"></iframe>
<img src="https://bad.example/pixel" onerror="alert(1)">
![image label](https://bad.example/pixel)
[bad](javascript:alert%281%29)
[local](file:///secret)
[good](https://example.com)
<a href="java&#x73;cript:alert(1)" onclick="alert(1)">raw</a>
'''
        doc = builder.build_document('Title', '', [('Heading', source)])
        self.assertIn('<table>', doc)
        self.assertIn('<td>A</td>', doc)
        self.assertIn('image label', doc)
        self.assertIn('href="https://example.com"', doc)
        self.assertNotIn('<script', doc)
        self.assertNotIn('<iframe', doc)
        self.assertNotIn('<img', doc)
        self.assertNotIn('href="javascript:', doc)
        self.assertNotIn('href="file:', doc)
        self.assertNotIn(' onclick=', doc)
        self.assertIn('Content-Security-Policy', doc)
        self.assertIn("default-src 'none'", doc)


class PdfTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = pathlib.Path(self.temp.name) / 'result.pdf'

    @staticmethod
    def write_pdf(args, **kwargs):
        target = next(arg.split('=', 1)[1] for arg in args
                      if arg.startswith('--print-to-pdf='))
        pathlib.Path(target).write_bytes(b'%PDF-1.7\nnew PDF\n%%EOF\n')
        return subprocess.CompletedProcess(args, 0)

    def test_renders_unique_temp_pdf_and_publishes_verified_result(self):
        with mock.patch.object(builder.subprocess, 'run', side_effect=self.write_pdf) as run:
            builder.render_pdf('<html>test</html>', self.out, 'browser', timeout=12)
        self.assertTrue(self.out.read_bytes().startswith(b'%PDF-'))
        args = run.call_args.args[0]
        self.assertNotIn('--print-to-pdf=' + str(self.out), args)
        self.assertEqual(run.call_args.kwargs['timeout'], 12)
        self.assertTrue(any(arg.startswith('--user-data-dir=') for arg in args))
        self.assertEqual(list(self.out.parent.iterdir()), [self.out])

    def test_existing_output_is_never_overwritten(self):
        self.out.write_bytes(b'old PDF')
        with mock.patch.object(builder.subprocess, 'run') as run:
            with self.assertRaisesRegex(builder.BuildError, 'already exists'):
                builder.render_pdf('html', self.out, 'browser', timeout=10)
        run.assert_not_called()
        self.assertEqual(self.out.read_bytes(), b'old PDF')

    def test_concurrent_output_is_not_clobbered(self):
        def concurrent_write(args, **kwargs):
            self.write_pdf(args, **kwargs)
            self.out.write_bytes(b'another writer')
        with mock.patch.object(builder.subprocess, 'run', side_effect=concurrent_write):
            with self.assertRaisesRegex(builder.BuildError, 'already exists'):
                builder.render_pdf('html', self.out, 'browser', timeout=10)
        self.assertEqual(self.out.read_bytes(), b'another writer')

    def test_missing_empty_and_non_pdf_results_are_rejected(self):
        for content in (None, b'', b'not PDF'):
            def invalid_write(args, **kwargs):
                if content is not None:
                    target = next(arg.split('=', 1)[1] for arg in args
                                  if arg.startswith('--print-to-pdf='))
                    pathlib.Path(target).write_bytes(content)
            with self.subTest(content=content):
                with mock.patch.object(builder.subprocess, 'run', side_effect=invalid_write):
                    with self.assertRaisesRegex(builder.BuildError, 'PDF'):
                        builder.render_pdf('html', self.out, 'browser', timeout=10)
                self.assertFalse(self.out.exists())
                self.assertEqual(list(self.out.parent.iterdir()), [])

    def test_timeout_and_browser_failure_report_clear_errors(self):
        for error, message in (
            (subprocess.TimeoutExpired('browser', 10), 'timed out'),
            (subprocess.CalledProcessError(2, 'browser', stderr='bad render'), 'exit code 2'),
            (OSError('cannot execute'), 'Cannot start browser'),
        ):
            with self.subTest(error=error):
                with mock.patch.object(builder.subprocess, 'run', side_effect=error):
                    with self.assertRaisesRegex(builder.BuildError, message):
                        builder.render_pdf('html', self.out, 'browser', timeout=10)
                self.assertFalse(self.out.exists())

    def test_browser_explicit_path_and_missing_path(self):
        executable = self.out.parent / 'browser.exe'
        executable.touch()
        self.assertEqual(builder.find_chrome(str(executable)), str(executable))
        with self.assertRaisesRegex(builder.BuildError, 'Browser not found'):
            builder.find_chrome(str(self.out.parent / 'absent.exe'))

    def test_browser_path_discovery(self):
        with mock.patch.object(builder, 'CHROME_CANDIDATES', []):
            with mock.patch.object(builder.shutil, 'which', return_value='/bin/chromium'):
                self.assertEqual(builder.find_chrome(), '/bin/chromium')

    def test_no_browser_and_unrelated_publish_error(self):
        with mock.patch.object(builder, 'CHROME_CANDIDATES', []):
            with mock.patch.object(builder.shutil, 'which', return_value=None):
                with self.assertRaisesRegex(builder.BuildError, '--browser'):
                    builder.find_chrome()
        with mock.patch.object(builder.subprocess, 'run', side_effect=self.write_pdf):
            with mock.patch.object(builder.os, 'link', side_effect=OSError(errno.EIO, 'disk error')):
                with self.assertRaisesRegex(builder.BuildError, 'disk error'):
                    builder.render_pdf('html', self.out, 'browser', timeout=10)
        self.assertFalse(self.out.exists())

    def test_unsupported_links_use_exclusive_copy_and_fsync(self):
        with mock.patch.object(builder.subprocess, 'run', side_effect=self.write_pdf):
            with mock.patch.object(builder.os, 'link', side_effect=OSError(errno.ENOTSUP, 'unsupported')):
                with mock.patch.object(builder.os, 'fsync', wraps=builder.os.fsync) as fsync:
                    builder.render_pdf('html', self.out, 'browser', timeout=10)
        self.assertTrue(self.out.read_bytes().startswith(b'%PDF-'))
        fsync.assert_called_once()

    def test_exclusive_copy_race_preserves_other_writer(self):
        def link_failure(*args):
            self.out.write_bytes(b'another writer')
            raise OSError(errno.ENOTSUP, 'unsupported')
        with mock.patch.object(builder.subprocess, 'run', side_effect=self.write_pdf):
            with mock.patch.object(builder.os, 'link', side_effect=link_failure):
                with self.assertRaisesRegex(builder.BuildError, 'already exists'):
                    builder.render_pdf('html', self.out, 'browser', timeout=10)
        self.assertEqual(self.out.read_bytes(), b'another writer')

    def test_failed_copy_or_fsync_removes_owned_partial_file(self):
        def failed_copy(source, target):
            target.write(b'partial')
            raise OSError(errno.ENOSPC, 'disk full')
        for name, effect in (('copyfileobj', failed_copy), ('fsync', OSError('flush failed'))):
            with self.subTest(stage=name):
                owner = builder.shutil if name == 'copyfileobj' else builder.os
                with mock.patch.object(builder.subprocess, 'run', side_effect=self.write_pdf):
                    with mock.patch.object(builder.os, 'link', side_effect=OSError(errno.ENOTSUP, 'unsupported')):
                        with mock.patch.object(owner, name, side_effect=effect):
                            with self.assertRaisesRegex(builder.BuildError, 'copy PDF'):
                                builder.render_pdf('html', self.out, 'browser', timeout=10)
                self.assertFalse(self.out.exists())
                self.assertEqual(list(self.out.parent.iterdir()), [])

    def test_fallback_source_error_cleans_empty_output(self):
        with self.assertRaisesRegex(builder.BuildError, 'copy PDF'):
            builder.exclusive_copy(self.out.parent / 'missing.pdf', self.out)
        self.assertFalse(self.out.exists())

    def test_fallback_cleanup_preserves_replacement(self):
        def replace_then_fail(source, target):
            target.close()
            self.out.unlink()
            self.out.write_bytes(b'replacement')
            raise OSError('copy failed')
        with mock.patch.object(builder.subprocess, 'run', side_effect=self.write_pdf):
            with mock.patch.object(builder.os, 'link', side_effect=OSError(errno.ENOTSUP, 'unsupported')):
                with mock.patch.object(builder.shutil, 'copyfileobj', side_effect=replace_then_fail):
                    with self.assertRaisesRegex(builder.BuildError, 'copy PDF'):
                        builder.render_pdf('html', self.out, 'browser', timeout=10)
        self.assertEqual(self.out.read_bytes(), b'replacement')

    def test_cli_success_and_input_errors(self):
        source = self.out.parent / 'chapter.md'
        source.write_text('# Chapter\ntext', encoding='utf-8-sig')
        args = ['--out', str(self.out), '--title', 'Test', str(source)]
        with mock.patch.object(builder, 'find_chrome', return_value='browser'):
            with mock.patch.object(builder.subprocess, 'run', side_effect=self.write_pdf):
                with contextlib.redirect_stdout(io.StringIO()) as printed:
                    self.assertEqual(builder.main(args), 0)
        self.assertIn(str(self.out), printed.getvalue())
        with contextlib.redirect_stderr(io.StringIO()) as errors:
            with self.assertRaises(SystemExit) as failure:
                builder.main(['--timeout', '0', *args])
        self.assertEqual(failure.exception.code, 2)
        self.assertIn('positive', errors.getvalue())
        with contextlib.redirect_stderr(io.StringIO()) as errors:
            self.assertEqual(builder.main(args[:-1] + [str(source) + '.missing']), 1)
        self.assertIn('Readout build failed', errors.getvalue())


if __name__ == '__main__':
    unittest.main()
