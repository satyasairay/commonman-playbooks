"""Assertions against the actual TEST build (run after Hugo)."""
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Resources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.loads = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'script':
            self.scripts.append(attrs)
        for key in ['src', 'srcset', 'poster', 'data']:
            if key in attrs:
                self.loads.append(attrs[key])
        if tag == 'link' and attrs.get('rel') in {'stylesheet', 'preload', 'prefetch', 'modulepreload', 'icon'}:
            self.loads.append(attrs.get('href', ''))


class BuildTests(unittest.TestCase):
    def test_reference_and_evidence_render(self):
        page = ROOT / '.cache/test-public/playbooks/test-page/index.html'
        self.assertTrue(page.exists(), 'build the TEST site first')
        html = page.read_text(encoding='utf-8')
        self.assertIn('data-fact="TEST-STEP-01">Read the test note.', html)
        self.assertIn('data-contact="C99"', html)
        self.assertIn('<details id="evidence-TEST-STEP-01"', html)
        self.assertIn('<blockquote>Read the test note.</blockquote>', html)
        parser = Resources()
        parser.feed(html)
        self.assertEqual(parser.loads, ['/site.css'])
        self.assertFalse(parser.scripts)
        css = (ROOT / '.cache/test-public/site.css').read_text(encoding='utf-8')
        self.assertNotIn('url(', css)
        self.assertNotIn('@import', css)


if __name__ == '__main__':
    unittest.main()
