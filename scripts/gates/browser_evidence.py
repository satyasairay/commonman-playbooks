"""CI browser evidence without adding any script or request to the site."""
import functools
import http.server
import json
import shutil
import subprocess
import struct
import threading
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]


def main():
    chrome = shutil.which('google-chrome') or shutil.which('google-chrome-stable') or shutil.which('chromium')
    if not chrome:
        raise SystemExit('browser evidence unavailable: no Chrome/Chromium on this CI runner')
    public = ROOT / '.cache/test-public'
    evidence = ROOT / '.cache/evidence'
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(public))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    url = f'http://127.0.0.1:{port}/playbooks/test-page/'
    path = public / 'playbooks/test-page/index.html'
    backup = ROOT / '.cache/mutations/browser-page.html.backup'
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, backup)
    version = subprocess.check_output([chrome, '--version'], text=True).strip()
    logs = []
    try:
        for state in ['closed', 'expanded']:
            if state == 'expanded':
                path.write_text(path.read_text(encoding='utf-8').replace('<details ', '<details open '), encoding='utf-8')
            log = evidence / f'browser-{state}-network.json'
            screenshot = evidence / f'web-320-{state}.png'
            command = [chrome, '--headless', '--no-sandbox', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--disable-background-networking', '--disable-component-update', '--disable-sync', '--disable-extensions', '--disable-features=Translate,MediaRouter,OptimizationHints', '--force-device-scale-factor=1', '--window-size=320,1400', '--hide-scrollbars', '--virtual-time-budget=1500', f'--user-data-dir={ROOT / (".cache/browser-" + state)}', f'--screenshot={screenshot}', f'--log-net-log={log}', url]
            result = subprocess.run(command, capture_output=True, text=True, timeout=60)
            if result.returncode or not screenshot.exists():
                raise SystemExit(result.stderr or 'browser did not create a screenshot')
            dimensions = struct.unpack('>II', screenshot.read_bytes()[16:24])
            if dimensions != (320, 1400):
                raise SystemExit(f'browser screenshot dimensions differ: {dimensions}')
            network = json.loads(log.read_text(encoding='utf-8'))
            requests = sorted({event.get('params', {}).get('url', '') for event in network.get('events', []) if event.get('params', {}).get('url', '').startswith(('http://', 'https://'))})
            outside = [request for request in requests if urlsplit(request).hostname != '127.0.0.1']
            if outside:
                raise SystemExit('browser recorded external requests: ' + repr(outside))
            logs.append({'state': state, 'width': 320, 'height': 1400, 'dpr': 1, 'browser': version, 'url': url, 'requests': requests, 'outside_requests': outside, 'screenshot': screenshot.name})
    finally:
        shutil.copyfile(backup, path)
        server.shutdown()
        server.server_close()
    (evidence / 'browser-evidence.json').write_text(json.dumps(logs, indent=2), encoding='utf-8')
    print(json.dumps(logs, indent=2))


if __name__ == '__main__':
    main()
