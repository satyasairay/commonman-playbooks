"""The browser capture must reject an outside request from the page target."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/gates'))
from browser_evidence import check_page_requests
import browser_evidence
import tempfile


class BrowserEvidenceTests(unittest.TestCase):
    def test_S9_every_built_page_and_print_are_selected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ('index.html', 'playbooks/test/index.html', 'playbooks/test/print.html', 'method/index.html'):
                file = root / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text('TEST', encoding='utf-8')
            self.assertEqual(browser_evidence.built_pages(root), ['index.html', 'method/index.html', 'playbooks/test/index.html', 'playbooks/test/print.html'])

    def test_empty_trace_fails_closed(self):
        with self.assertRaises(ValueError):
            check_page_requests([])

    def test_page_origin_control(self):
        events = [{'method': 'Network.requestWillBeSent', 'params': {'request': {'url': 'http://127.0.0.1:8765/site.css'}}}]
        self.assertEqual(check_page_requests(events), ['http://127.0.0.1:8765/site.css'])
        events.append({'method': 'Network.requestWillBeSent', 'params': {'request': {'url': 'https://example.invalid/track'}}})
        with self.assertRaises(ValueError):
            check_page_requests(events)


if __name__ == '__main__':
    unittest.main()
