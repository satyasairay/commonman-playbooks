"""The browser capture must reject an outside request from the page target."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/gates'))
from browser_evidence import check_page_requests
import browser_evidence
import tempfile
import threading
import socket


class BrowserEvidenceTests(unittest.TestCase):
    def test_idle_connection_uses_current_build_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first, second = root / 'first', root / 'second'
            first.mkdir()
            second.mkdir()
            (first / 'index.html').write_text('OLD', encoding='utf-8')
            (second / 'index.html').write_text('CURRENT', encoding='utf-8')
            server = browser_evidence.build_server(first)
            ready = threading.Event()
            original = server.RequestHandlerClass
            class ReadyHandler(original):
                def setup(self):
                    super().setup()
                    ready.set()
            server.RequestHandlerClass = ReadyHandler
            threading.Thread(target=server.serve_forever, daemon=True).start()
            try:
                with socket.create_connection(server.server_address, timeout=3) as connection:
                    self.assertTrue(ready.wait(3))
                    server.build_directory = str(second)
                    connection.sendall(b'GET /index.html HTTP/1.0\r\nHost: localhost\r\n\r\n')
                    with connection.makefile('rb') as response:
                        self.assertEqual(response.read().split(b'\r\n\r\n', 1)[1], b'CURRENT')
            finally:
                server.shutdown()
                server.server_close()

    def test_missing_page_or_stylesheet_fails(self):
        events = [{'method': 'Network.requestWillBeSent', 'params': {'request': {'url': 'http://127.0.0.1:8765/site.css'}}}, {'method': 'Network.responseReceived', 'params': {'response': {'url': 'http://127.0.0.1:8765/site.css', 'status': 404}}}]
        with self.assertRaises(ValueError):
            check_page_requests(events)

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
