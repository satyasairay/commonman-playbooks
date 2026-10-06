"""Break each site/source control only in a disposable repository copy."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from record_run import ROOT, redact

MUTATIONS = [
    ('S14', 'layouts/partials/confidence.html', 'i18n "confirmed_by" (dict "agency" $row.source_owner "date" (time.Format "2 January 2006" $row.verified_on))', 'i18n "confirmed"'),
    ('S16', 'hugo.toml', "disableLanguages = ['or', 'hi']", "disableLanguages = []"),
    ('S17', 'layouts/partials/trust.html', 'data-overdue', 'data-removed'),
    ('S18', 'layouts/_default/baseof.html', 'substr (getenv "BUILD_COMMIT") 0 7', 'getenv "BUILD_COMMIT"'),
    ('S19', 'layouts/_default/single.html', '<h2>{{ i18n "clock" }}</h2><ul>', '<ul>'),
    ('S21', 'scripts/sources/fetch.py', "if any((folder / (sid + ext)).exists() for ext in ('.html', '.pdf', '.txt')):", 'if False:'),
    ('export-isolation', 'scripts/facts/export.py', "if args.output.resolve() == (ROOT / 'data/generated').resolve() and", 'if False and'),
    ('source-id', 'scripts/facts/registry.py', 'if not SOURCE_ID.fullmatch(value):', 'if False:'),
    ('https-redirect', 'scripts/sources/fetch_text.py', "if not newurl.lower().startswith('https://'):", 'if False:'),
    ('page-recheck', 'layouts/partials/trust.html', '.Params.recheck_by | default ""', '""'),
    ('footer-ai', 'layouts/_default/baseof.html', 'data-ai-line', 'data-removed'),
    ('privacy', 'hugo.toml', "urls = ['none']", "urls = ['.*']"),
]

def copy_repo(target):
    for name in ('scripts', 'tests', 'rules', 'layouts', 'static', 'i18n', 'content'):
        shutil.copytree(ROOT / name, target / name, ignore=shutil.ignore_patterns('__pycache__', 'evidence'))
    shutil.copy2(ROOT / 'hugo.toml', target / 'hugo.toml')

def run(root, args):
    env = dict(os.environ, PYTHONUTF8='1', BUILD_COMMIT='abcdef0123456789abcdef0123456789abcdef01', BUILD_DATE='2026-10-06')
    return subprocess.run(args, cwd=root, env=env, capture_output=True, text=True, encoding='utf-8')

def build(root):
    for args in ([sys.executable, 'scripts/facts/export.py', '--facts', 'tests/fixtures/registries/facts.md', '--contacts', 'tests/fixtures/registries/contacts.md', '--output', '.cache/fixture-data/generated'], ['hugo', '--config', 'hugo.toml,tests/fixtures/hugo.toml', '-D', '--cleanDestinationDir', '--destination', '.cache/test-public', '--panicOnWarning']):
        result = run(root, args)
        if result.returncode:
            raise RuntimeError(redact(result.stdout + result.stderr))

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    logs = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / 'repo'
        root.mkdir()
        copy_repo(root)
        for name, path, old, new in MUTATIONS:
            file = root / path
            backup = file.with_name(file.name + '.backup')
            shutil.copy2(file, backup)
            text = file.read_text(encoding='utf-8')
            if text.count(old) != 1:
                raise RuntimeError(f'{name}: mutation target count is {text.count(old)}')
            file.write_text(text.replace(old, new), encoding='utf-8')
            build(root)
            red = run(root, [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_fix_site.py', '-v'])
            if red.returncode == 0 or 'FAILED' not in red.stderr:
                raise RuntimeError(f'{name}: test did not detect disabled control')
            shutil.copy2(backup, file)
            build(root)
            green = run(root, [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_fix_site.py', '-v'])
            if green.returncode:
                raise RuntimeError(f'{name}: restored tests failed\n{green.stderr}')
            log = f'{name}: disabled RED exit {red.returncode}; backup restored GREEN exit {green.returncode}\n' + red.stderr + green.stderr
            logs.append(log.replace(str(root), '<temp-repo>'))
            print(logs[-1].splitlines()[0])
    destination = ROOT / 'tests/evidence/L03-fix-a/mutations.txt'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(redact('\n'.join(logs)), encoding='utf-8')

if __name__ == '__main__':
    main()
