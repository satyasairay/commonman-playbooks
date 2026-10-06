"""Independent control mutations in TemporaryDirectory copies only."""
import copy
import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from gates import Context, ROOT, check_document
sys.path.insert(0, str(ROOT / 'tests'))
from site_mutations import copy_repo, build, run

CONTROLS = [
    ('B1-source', 'gates.py', 'if step and int(step[1]) == expected:', 'if step:'),
    ('B1-built', 'gates.py', "if tag == 'ol' and str(attrs.get('start', '1')) != '1':", 'if False:'),
    ('B2', 'gates.py', 'if claims and (BARE.search(text) or LEGAL_CAPITAL.search(text)):', 'if False:'),
    ('S1', 'english.py', "blocks = re.split(r'\\n\\s*\\n', text)", "blocks = text.splitlines()"),
    ('S2-deny', 'english.py', "if normal in {'paisa', 'karein', 'jaldi', 'ji', 'didi', 'saathi', 'nyaya', 'beta', 'bas', 'na'} or normal not in dictionary:", 'if normal not in dictionary:'),
    ('S2-phrases', 'english.py', "out.update(term.strip().lower() for term in cells[0].split(','))", "out.update(w.lower() for w in re.findall(r'[A-Za-z]+', cells[0]))"),
    ('S3', 'gates.py', 'for value in LINK.findall(text):', 'for value in []:'),
    ('S4-raw', 'gates.py', 'if INTERNAL.search(body):', 'if False:'),
    ('S5', 'gates.py', "if section in {'playbooks', 'cards'} and meta.get('kind') != {'playbooks': 'playbook', 'cards': 'card'}[section]:", 'if False:'),
    ('S6', 'gates.py', "if path.suffix != '.md':", 'if False:'),
    ('S7', 'gates.py', "if row['kind'] not in KINDS:", 'if False:'),
    ('S8-script', 'gates.py', "if doc.language == 'en' and re.search(r'[\\u0900-\\u097f\\u0b00-\\u0b7f]', content):", 'if False:'),
    ('S8-verifier', 'gates.py', "['title', 'scope_covers', 'scope_excludes', 'verified_by']", "['title', 'scope_covers', 'scope_excludes']"),
    ('S9-style', 'gates.py', "if re.search(r'url\\s*\\(|@import|@font-face', ''.join(doc.styles), re.I):", 'if False:'),
    ('S9-attributes', 'gates.py', "if re.search(r'(?:https?:)?//', value, re.I) and not (key == 'href' and 'data-contact' in attrs):", 'if False:'),
    ('S10', 'gates.py', "if production and meta.get('draft') is True:", 'if False:'),
    ('S11-sha', 'gates.py', "if not re.fullmatch(r'[0-9a-fA-F]{7,40}', identity.get('data-build-commit') or ''):", 'if False:'),
    ('S11-date', 'gates.py', "parse_date(identity.get('data-build-date', ''))", "parse_date('2026-10-06')"),
    ('S12-https', 'gates.py', "url.scheme != 'https' or url.username or", 'url.username or'),
    ('S12-username', 'gates.py', "url.scheme != 'https' or url.username or", "url.scheme != 'https' or"),
    ('S12-signature', 'gates.py', "    if meta.get('draft') is False:\n        try:", '    if False:\n        try:'),
    ('S12-recheck-boundary', 'gates.py', "parse_date(row['recheck_by']) <= ctx.today", "parse_date(row['recheck_by']) < ctx.today"),
    ('S12-confidence', 'gates.py', "if meta.get('kind') == 'card' and meta.get('confidence') not in {'watch', 'confirmed'}:", 'if False:'),
    ('S12-required-pages', 'gates.py', "if not (Path(public) / path).exists():", 'if False:'),
    ('S12-live-build', 'gates.py', "elif meta.get('draft') is False:", 'elif False:'),
    ('S12-loop-id', 'gates.py', r'\bL\d\d[a-z]?(?:-cx)?\b|', ''),
    ('S12-internal-path', 'gates.py', r'(?:rules|content|scripts|loops)[/\\]|', ''),
    ('S12-call-short', 'gates.py', r'|\b(?:call|dial|helpline|phone)\s+\d{3,5}\b', ''),
    ('G6', 'gates.py', "if not ctx.no_contact.get(doc.language) or ctx.no_contact[doc.language] not in lines:", 'if False:'),
    ('G8', 'gates.py', 'if not expected or not visible or norm(visible[0]) != expected:', 'if False:'),
    ('fact-sentence', 'gates.py', "prose.setdefault(attrs.get('_block', line), []).append(content)\n        elif 'data-contact'", "pass\n        elif 'data-contact'"),
    ('footer-ai', 'gates.py', "if not any('data-ai-line' in a and a.get('data-frame') == 'footer' for a in doc.attrs):", 'if False:'),
    ('web-size', 'gates.py', "if len(text.encode('utf-8')) >= 50000:", 'if False:'),
    ('S22', '../facts/registry.py', "raise ValueError('date must be YYYY-MM-DD or day full-month year (for example 6 October 2026)')", 'return dt.date(2026, 10, 6)'),
    ('network-pages', 'browser_evidence.py', "return sorted(path.relative_to(public).as_posix() for path in Path(public).rglob('*.html'))", "return ['index.html']"),
    ('verified-only', '../facts/export.py', "if row['status'] == 'verified'", 'if True'),
    ('source-script', '../sources/fetch_text.py', '"script", "style",', '"style",'),
    ('S12-share-parity', 'gates.py', "return [Error('G12', 'share link text differs from source page')] if any(text != canonical for text in shares) else []", 'return []'),
]

def fixture_mutations():
    ctx = Context.fixture()
    handwritten = (ROOT / 'tests/fixtures/gates/page.html').read_text(encoding='utf-8')
    built = (ROOT / '.cache/test-public/playbooks/test-page/index.html').read_text(encoding='utf-8')
    signed = (ROOT / '.cache/test-public/playbooks/test-signed/index.html').read_text(encoding='utf-8')
    for item in json.loads((ROOT / 'tests/fixtures/gates/mutations.json').read_text(encoding='utf-8')):
        for surface in ('handwritten', 'Hugo-built'):
            baseline = handwritten if surface == 'handwritten' else signed if item['gate'] == 'G3' else built
            changed, context = baseline, copy.deepcopy(ctx)
            if item['target'] == 'fact':
                context.facts['TEST-STEP-01'][item['field']] = item['new']
                if 'kind' in item:
                    context.facts['TEST-STEP-01']['kind'] = item['kind']
            elif surface == 'handwritten':
                changed = baseline.replace(item['old'], item['new'])
            elif item['gate'] == 'G3':
                changed = re.sub(r'<p data-verified-by>.*?</p>', '', baseline)
            elif item['gate'] in {'G6', 'G8'}:
                marker = 'data-no-contact' if item['gate'] == 'G6' else 'data-opening'
                changed = re.sub(r'<p[^>]*' + marker + r'[^>]*>.*?</p>', '', baseline)
            else:
                changed = baseline.replace(item['old'], item['new'])
            errors = check_document(changed, context, require_trust=surface == 'handwritten' or item['gate'] == 'G3')
            if item['gate'] not in {e.gate for e in errors}:
                raise RuntimeError(f'{surface} {item}: mutation survived')
            restored = check_document(baseline, ctx, require_trust=surface == 'handwritten' or item['gate'] == 'G3')
            if restored:
                raise RuntimeError(f'{surface}: baseline not green: {restored}')
            print(f'{item["gate"]} {surface}: RED; backup baseline GREEN')

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument('--only')
    args = parser.parse_args()
    fixture_mutations()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / 'repo'
        root.mkdir()
        copy_repo(root)
        build(root)
        for name, path, old, new in CONTROLS:
            if args.only and name != args.only:
                continue
            file = root / 'scripts/gates' / path
            text = file.read_text(encoding='utf-8')
            if text.count(old) != 1:
                raise RuntimeError(f'{name}: target count {text.count(old)}')
            backup = file.with_name(file.name + '.backup')
            shutil.copy2(file, backup)
            file.write_text(text.replace(old, new), encoding='utf-8')
            pattern = 'test_share_control.py' if name == 'S12-share-parity' else 'test_browser_evidence.py' if name == 'network-pages' else 'test_registry.py' if name in {'verified-only', 'source-script'} else 'test_gate*.py'
            command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', pattern, '-v']
            red = run(root, command)
            if red.returncode == 0 or 'FAIL:' not in red.stderr or 'ERROR:' in red.stderr:
                raise RuntimeError(f'{name}: mutation not killed by an assertion\n{red.stderr}')
            print(f'{name} disabled alone: RED exit {red.returncode}', flush=True)
            print(red.stderr.replace(str(root), '<temp-repo>'))
            shutil.copy2(backup, file)
            green = run(root, command)
            if green.returncode:
                raise RuntimeError(f'{name}: backup restore not green\n{green.stderr}')
            print(f'{name} backup restored: GREEN exit {green.returncode}', flush=True)

if __name__ == '__main__':
    main()
