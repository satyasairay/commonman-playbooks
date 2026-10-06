"""Fetch registry sources; emit hash proposals without editing protected rules."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'facts'))
from registry import ROOT, read, source_id
from fetch_text import fetch, to_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', action='append', help='source ids; default all registry sources')
    args = parser.parse_args()
    _, _, sources = read(ROOT / 'rules/facts.md', ROOT / 'rules/contacts.md')
    folder = ROOT / '.cache/sources'
    folder.mkdir(parents=True, exist_ok=True)
    manifest = {}
    ids = list(args.id or sources)
    for sid in ids:
        source_id(sid)
        if sid not in sources:
            parser.error(f'unknown source: {sid}')
        if any((folder / (sid + ext)).exists() for ext in ('.html', '.pdf', '.txt')):
            raise SystemExit(f'{sid}: snapshot exists; preserve it for Satya and use a new source id')
    for sid in ids:
        raw, ctype, final = fetch(sources[sid]['url'])
        # Stop on an access challenge; never try another identity or route.
        if b'captcha' in raw.lower() or b'cf-chl-' in raw.lower():
            raise SystemExit(f'{sid}: access challenge; Satya must supply a snapshot')
        ext = '.pdf' if raw[:5] == b'%PDF-' else '.html'
        path = folder / (sid + ext)
        with path.open('xb') as saved:
            saved.write(raw)
        text = to_text(path, raw)
        with (folder / (sid + '.txt')).open('x', encoding='utf-8') as saved:
            saved.write(text)
        manifest[sid] = {'sha256': hashlib.sha256(raw).hexdigest(), 'final_url': final, 'content_type': ctype}
        print(sid, manifest[sid]['sha256'])
    (folder / 'hash-proposals.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print('Hash proposals saved; only Satya may update rules/facts.md.')


if __name__ == '__main__':
    main()
