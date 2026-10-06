"""One PC/CI entry point. Build previews, test controls and retain evidence."""
import argparse
import datetime as dt
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def command(args, name, env):
    result = subprocess.run(args, cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
    output = result.stdout + result.stderr
    (ROOT / '.cache/evidence' / (name + '.txt')).write_text(output, encoding='utf-8')
    if name in {'mutations', 'format-controls', 'format-mutations'}:
        print('\n'.join(line for line in output.splitlines() if line.startswith(('G1', 'G2', 'G3', 'G4', 'G6', 'G7', 'G8', 'G9', 'verified-only', 'source script', 'built resource', 'page network'))))
    else:
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
    env['BUILD_COMMIT'] = env.get('GITHUB_SHA') or subprocess.check_output(['git', '-c', f'safe.directory={ROOT.as_posix()}', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, text=True).strip()
    env['BUILD_DATE'] = dt.datetime.now(dt.timezone.utc).date().isoformat()
    command([sys.executable, 'scripts/facts/export.py'], 'real-export', env)
    command([sys.executable, 'scripts/facts/formats.py'], 'real-formats', env)
    command([args.hugo, '--buildDrafts', '--panicOnWarning'], 'real-preview-build', env)
    command([sys.executable, 'scripts/gates/gates.py'], 'real-gates', env)
    command([sys.executable, 'scripts/facts/export.py', '--facts', 'tests/fixtures/registries/facts.md', '--contacts', 'tests/fixtures/registries/contacts.md', '--output', '.cache/fixture-data/generated'], 'test-export', env)
    command([sys.executable, 'scripts/facts/formats.py', '--content', 'tests/fixtures/site', '--facts', 'tests/fixtures/registries/facts.md', '--contacts', 'tests/fixtures/registries/contacts.md', '--output', '.cache/fixture-data/generated'], 'test-formats', env)
    command([args.hugo, '--config', 'hugo.toml,tests/fixtures/hugo.toml', '--buildDrafts', '--destination', '.cache/test-public', '--panicOnWarning'], 'test-build', env)
    command([sys.executable, 'scripts/gates/gates.py', '--content', 'tests/fixtures/site', '--public', '.cache/test-public', '--facts', 'tests/fixtures/registries/facts.md', '--contacts', 'tests/fixtures/registries/contacts.md'], 'test-gates', env)
    command([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], 'tests', env)
    command([sys.executable, '-B', 'scripts/gates/mutations.py'], 'mutations', env)
    command([sys.executable, '-B', 'scripts/gates/format_mutations.py', '--controls-only'], 'format-controls', env)
    print('Verification GREEN. Preview only; no publication or human approval implied.')


if __name__ == '__main__':
    main()
