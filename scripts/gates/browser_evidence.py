"""Capture actual page-network events and pixels in an isolated CI browser."""
import base64
import functools
import http.server
import json
import shutil
import struct
import subprocess
import tempfile
import threading
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit
from cdp import Client

ROOT = Path(__file__).resolve().parents[2]


def check_page_requests(events):
    requests = []
    for event in events:
        method = event.get('method', '')
        params = event.get('params', {})
        if method == 'Network.requestWillBeSent':
            requests.append(params['request']['url'])
        elif method in {'Network.webSocketCreated', 'Network.webTransportCreated'}:
            requests.append(params['url'])
    requests = sorted(set(requests))
    outside = [url for url in requests if urlsplit(url).hostname not in {'127.0.0.1', 'localhost'}]
    if not requests or outside:
        raise ValueError('empty page trace or external requests: ' + repr(outside))
    return requests


def main():
    chrome = shutil.which('google-chrome') or shutil.which('google-chrome-stable') or shutil.which('chromium')
    if not chrome:
        raise SystemExit('browser evidence unavailable: no Chrome/Chromium on this CI runner')
    evidence = ROOT / '.cache/evidence'
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT / '.cache/test-public'))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f'http://127.0.0.1:{server.server_address[1]}/playbooks/test-page/'
    version = subprocess.check_output([chrome, '--version'], text=True).strip()
    records = []
    client = None
    with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as profile:
        assert Path(profile).resolve().is_relative_to(ROOT.resolve())
        diagnostic = (evidence / 'browser-driver.txt').open('w', encoding='utf-8')
        process = subprocess.Popen([chrome, '--headless', '--no-sandbox', '--disable-gpu', '--no-first-run', '--disable-background-networking', '--disable-extensions', '--remote-debugging-address=127.0.0.1', '--remote-debugging-port=0', f'--user-data-dir={profile}', 'about:blank'], stdout=subprocess.DEVNULL, stderr=diagnostic)
        try:
            active = Path(profile) / 'DevToolsActivePort'
            deadline = time.monotonic() + 20
            while not active.exists():
                if process.poll() is not None or time.monotonic() > deadline:
                    raise OSError('Chrome failed to open a local test protocol port; see browser-driver.txt')
                time.sleep(.05)
            port = int(active.read_text().splitlines()[0])
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list', timeout=10) as response:
                targets = json.load(response)
            target = next(row for row in targets if row['type'] == 'page' and row['url'] == 'about:blank')
            client = Client(target['webSocketDebuggerUrl'])
            client.command('Network.enable')
            client.command('Page.enable')
            client.command('Page.setLifecycleEventsEnabled', enabled=True)
            client.command('Emulation.setDeviceMetricsOverride', width=320, height=1400, deviceScaleFactor=1, mobile=True)
            start = len(client.events)
            navigation = client.command('Page.navigate', url=url)
            if navigation.get('errorText'):
                raise OSError(navigation['errorText'])
            client.wait_for('Page.lifecycleEvent', start, name='load', loaderId=navigation['loaderId'])
            root = client.command('DOM.getDocument')['root']['nodeId']
            details = client.command('DOM.querySelector', nodeId=root, selector='details')['nodeId']
            summary = client.command('DOM.querySelector', nodeId=root, selector='details summary')['nodeId']
            if not details or not summary:
                raise ValueError('the built evidence control is missing')
            for state in ['closed', 'expanded']:
                if state == 'expanded':
                    client.command('DOM.scrollIntoViewIfNeeded', nodeId=summary)
                    quad = client.command('DOM.getBoxModel', nodeId=summary)['model']['border']
                    x, y = sum(quad[0::2]) / 4, sum(quad[1::2]) / 4
                    client.command('Input.dispatchMouseEvent', type='mousePressed', x=x, y=y, button='left', clickCount=1)
                    client.command('Input.dispatchMouseEvent', type='mouseReleased', x=x, y=y, button='left', clickCount=1)
                attrs = client.command('DOM.getAttributes', nodeId=details)['attributes'][0::2]
                if ('open' in attrs) != (state == 'expanded'):
                    raise ValueError('native details did not reach the requested state')
                metrics = client.command('Page.getLayoutMetrics')
                if metrics['cssLayoutViewport']['clientWidth'] != 320 or metrics['cssContentSize']['width'] > 321:
                    raise ValueError('page viewport is not 320px or has horizontal overflow')
                png = base64.b64decode(client.command('Page.captureScreenshot', format='png', fromSurface=True)['data'])
                dimensions = struct.unpack('>II', png[16:24])
                if dimensions != (320, 1400):
                    raise ValueError(f'screenshot dimensions differ: {dimensions}')
                screenshot = evidence / f'web-320-{state}.png'
                screenshot.write_bytes(png)
                requests = check_page_requests(client.events)
                stylesheet = f'http://127.0.0.1:{server.server_address[1]}/site.css'
                if url not in requests or stylesheet not in requests:
                    raise ValueError('page and stylesheet requests missing from browser trace')
                records.append({'state': state, 'width': 320, 'height': 1400, 'dpr': 1, 'mobile_viewport': True, 'browser': version, 'url': url, 'requests': requests, 'outside_requests': [], 'screenshot': screenshot.name, 'ready': 'page load lifecycle event and loaded CSS'})
            network = [event for event in client.events if event.get('method', '').startswith('Network.')]
            (evidence / 'browser-page-network.json').write_text(json.dumps(network, indent=2), encoding='utf-8')
            (evidence / 'browser-evidence.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
            print(json.dumps(records, indent=2))
        finally:
            if client:
                client.close()
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            diagnostic.close()
            server.shutdown()
            server.server_close()


if __name__ == '__main__':
    main()
