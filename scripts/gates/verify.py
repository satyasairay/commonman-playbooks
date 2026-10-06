"""One PC/CI entry point. Build previews, test controls and retain evidence."""
import argparse
import datetime as dt
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tests'))
from record_run import redact


def command(args, name, env):
    result = subprocess.run(args, cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
    output = redact(result.stdout + result.stderr)
    (ROOT / '.cache/evidence' / (name + '.txt')).write_text(output, encoding='utf-8')
    print(output, end='')
    if result.returncode:
        raise SystemExit(f'{name}: command failed with exit {result.returncode}')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument('--hugo', default=shutil.which('hugo'))
    args = parser.parse_args()
    if not args.hugo:
        parser.error('Hugo executable required; pass --hugo path')
    (ROOT / '.cache/evidence').mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env['PYTHONUTF8'] = '1'
    env['BUILD_COMMIT'] = env.get('GITHUB_SHA') or subprocess.check_output(['git', '-c', f'safe.directory={ROOT.as_posix()}', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, text=True).strip()
    env['BUILD_DATE'] = dt.datetime.now(dt.timezone.utc).date().isoformat()
    command([sys.executable, 'scripts/facts/export.py'], 'real-export', env)
    if (ROOT / 'scripts/facts/formats.py').exists():
        command([sys.executable, 'scripts/facts/formats.py'], 'real-formats', env)
    command([args.hugo, '--cleanDestinationDir', '--panicOnWarning'], 'production-build', env)
    command([sys.executable, 'scripts/gates/gates.py', '--production'], 'production-gates', env)
    command([args.hugo, '--buildDrafts', '--cleanDestinationDir', '--destination', '.cache/preview-public', '--panicOnWarning'], 'real-preview-build', env)
    command([sys.executable, 'scripts/gates/gates.py', '--public', '.cache/preview-public'], 'real-gates', env)
    test_env = dict(env, BUILD_COMMIT='abcdef0123456789abcdef0123456789abcdef01', BUILD_DATE='2026-10-06')
    command([sys.executable, 'scripts/facts/export.py', '--facts', 'tests/fixtures/registries/facts.md', '--contacts', 'tests/fixtures/registries/contacts.md', '--output', '.cache/fixture-data/generated'], 'test-export', env)
    if (ROOT / 'scripts/facts/formats.py').exists():
        command([sys.executable, 'scripts/facts/formats.py', '--content', 'tests/fixtures/site', '--facts', 'tests/fixtures/registries/facts.md', '--contacts', 'tests/fixtures/registries/contacts.md', '--output', '.cache/fixture-data/generated'], 'test-formats', env)
    command([args.hugo, '--config', 'hugo.toml,tests/fixtures/hugo.toml', '--buildDrafts', '--cleanDestinationDir', '--destination', '.cache/test-public', '--panicOnWarning'], 'test-build', test_env)
    command([sys.executable, 'scripts/gates/gates.py', '--content', 'tests/fixtures/site', '--public', '.cache/test-public', '--facts', 'tests/fixtures/registries/facts.md', '--contacts', 'tests/fixtures/registries/contacts.md'], 'test-gates', env)
    command([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], 'tests', env)
    command([sys.executable, '-B', 'scripts/gates/mutations.py'], 'mutations', env)
    if (ROOT / 'scripts/gates/format_mutations.py').exists():
        command([sys.executable, '-B', 'scripts/gates/format_mutations.py', '--controls-only'], 'format-controls', env)
    formats = ROOT / 'scripts/gates/verify_formats.py'
    if formats.exists():
        try:
            import weasyprint
        except (ImportError, OSError):
            print('G12 NOT RUN: WeasyPrint is absent; the formats CI job is required.')
        else:
            command([sys.executable, str(formats)], 'formats', env)
    else:
        print('G12 NOT RUN: formats are implemented on L03c; its CI job is required.')
    print('Verification completed. No publication or human approval implied.')


if __name__ == '__main__':
    main()
