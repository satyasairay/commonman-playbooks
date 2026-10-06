"""Review regressions against Hugo's isolated TEST build and source tools."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/facts'))
sys.path.insert(0, str(ROOT / 'scripts/sources'))
import registry
import fetch as source_fetch
import fetch_text


class FixSiteTests(unittest.TestCase):
    def page(self, name='playbooks/test-page'):
        return (ROOT / '.cache/test-public' / name / 'index.html').read_text(encoding='utf-8')

    def test_S14_card_label_under_opening(self):
        html = self.page('cards/test-card')
        self.assertIn('Confirmed by TEST agency on 6 October 2026', html)
        self.assertLess(html.index('data-opening'), html.index('data-confidence'))
        self.assertLess(html.index('data-confidence'), html.index('<h1>'))

    def test_S16_deferred_languages(self):
        self.assertEqual(tomllib.loads((ROOT / 'hugo.toml').read_text())['disableLanguages'], ['or', 'hi'])
        self.assertFalse((ROOT / '.cache/test-public/or/index.html').exists())
        self.assertFalse((ROOT / '.cache/test-public/hi/index.html').exists())

    def test_S17_overdue_notice(self):
        self.assertIn('data-overdue', self.page('playbooks/test-signed'))

    def test_S18_readable_dates_short_commit(self):
        html = self.page()
        self.assertIn('Checked on 6 October 2026', html)
        self.assertIn('Build abcdef0', html)
        self.assertNotIn('Build abcdef0123456789', html)
        self.assertIn('6 October 2026', html)

    def test_S19_clock_heading_list_fact(self):
        html = self.page()
        self.assertRegex(html, r'(?s)<aside class="clock"[^>]*>\s*<h2>.*?</h2>\s*<ul>\s*<li>.*?data-fact="TEST-DEADLINE-01"')

    def test_signed_fixture_exact_line_and_page_recheck(self):
        html = self.page('playbooks/test-signed')
        self.assertIn('Verified by Satyasai Ray on 6 October 2026.', html)
        self.assertIn('Next check by 5 October 2026', html)
        self.assertIn('data-ai-line', html)

    def test_privacy_and_http_disabled(self):
        config = tomllib.loads((ROOT / 'hugo.toml').read_text())
        self.assertEqual(config['security']['http']['urls'], ['none'])
        for service in ('disqus', 'googleAnalytics', 'instagram', 'vimeo', 'x', 'youTube'):
            self.assertTrue(config['privacy'][service]['disable'])

    def test_fixture_export_refuses_default_output(self):
        run = subprocess.run([sys.executable, str(ROOT / 'scripts/facts/export.py'), '--facts', str(ROOT / 'tests/fixtures/registries/facts.md')], capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('explicit', run.stderr)

    def test_source_ids_closed_pattern(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'facts.md'
            path.write_text((ROOT / 'tests/fixtures/registries/facts.md').read_text().replace('src-test', '../../content/en/x'), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'source id'):
                registry.read(path, ROOT / 'tests/fixtures/registries/contacts.md')

    def test_S21_snapshot_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / '.cache/sources'
            folder.mkdir(parents=True)
            original = folder / 'src-test.txt'
            original.write_text('Satya checked this', encoding='utf-8')
            sources = {'src-test': {'url': 'https://rbi.org.in/test'}}
            with patch.object(source_fetch, 'ROOT', root), patch.object(source_fetch, 'read', return_value=({}, {}, sources)), patch.object(sys, 'argv', ['fetch.py']), patch.object(source_fetch, 'fetch', return_value=(b'<p>New</p>', 'text/html', sources['src-test']['url'])) as network:
                with self.assertRaisesRegex(SystemExit, 'snapshot exists'):
                    source_fetch.main()
                network.assert_not_called()
            self.assertEqual(original.read_text(), 'Satya checked this')

    def test_redirect_to_http_refused(self):
        handler = fetch_text.HTTPSRedirectHandler()
        import urllib.request
        req = urllib.request.Request('https://rbi.org.in/test')
        with self.assertRaisesRegex(ValueError, 'HTTPS'):
            handler.redirect_request(req, None, 302, 'Found', {}, 'http://rbi.org.in/test')


if __name__ == '__main__':
    unittest.main()
