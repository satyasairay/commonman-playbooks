"""The browser capture must reject an outside request from the page target."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/gates'))
from browser_evidence import check_page_requests


class BrowserEvidenceTests(unittest.TestCase):
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
