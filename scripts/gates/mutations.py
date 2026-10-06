"""Prove fixture failures and kill disabled controls; restore from byte backups."""
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path
from gates import Context, GATES, ROOT, check_document


def prove_control(path, backup, changed, pattern, label):
    shutil.copyfile(path, backup)
    try:
        path.write_text(changed, encoding='utf-8')
        command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', pattern, '-v']
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        assert result.returncode != 0, f'{label} disabled control survived'
        print(f'{label} disabled control: TESTS RED (expected)')
        print(result.stdout + result.stderr)
    finally:
        shutil.copyfile(backup, path)
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout + result.stderr
    print(f'{label} restored control: TESTS GREEN')
    print(result.stdout + result.stderr)


def main():
    folder = ROOT / '.cache/mutations'
    folder.mkdir(parents=True, exist_ok=True)
    source = ROOT / 'tests/fixtures/gates/page.html'
    active = folder / 'page.html'
    backup = folder / 'page.html.backup'
    shutil.copyfile(source, active)
    shutil.copyfile(active, backup)
    baseline = Context.fixture()
    mutations = json.loads((ROOT / 'tests/fixtures/gates/mutations.json').read_text(encoding='utf-8'))
    for index, item in enumerate(mutations, 1):
        ctx = copy.deepcopy(baseline)
        try:
            if item['target'] == 'html':
                original = active.read_text(encoding='utf-8')
                assert item['old'] in original
                active.write_text(original.replace(item['old'], item['new']), encoding='utf-8')
            else:
                registry = folder / 'facts.json'
                registry.write_text(json.dumps(ctx.facts), encoding='utf-8')
                shutil.copyfile(registry, folder / 'facts.json.backup')
                ctx.facts['TEST-STEP-01'][item['field']] = item['new']
                if 'kind' in item:
                    ctx.facts['TEST-STEP-01']['kind'] = item['kind']
                registry.write_text(json.dumps(ctx.facts), encoding='utf-8')
                ctx.facts = json.loads(registry.read_text(encoding='utf-8'))
            errors = check_document(active.read_text(encoding='utf-8'), ctx, require_trust=True)
            hits = [e for e in errors if e.gate == item['gate']]
            assert hits, f'mutation {index} survived'
            print(f'{item["gate"]} fixture {index}: RED (expected)')
            for error in hits:
                print(error)
        finally:
            shutil.copyfile(backup, active)
            if item['target'] == 'fact':
                shutil.copyfile(folder / 'facts.json.backup', folder / 'facts.json')
                ctx.facts = json.loads((folder / 'facts.json').read_text(encoding='utf-8'))
        restored = check_document(active.read_text(encoding='utf-8'), ctx, require_trust=True)
        assert not restored, restored
        print(f'{item["gate"]} fixture {index}: GREEN after backup restore')

    control = ROOT / 'scripts/gates/gates.py'
    control_backup = folder / 'gates.py.backup'
    shutil.copyfile(control, control_backup)
    try:
        for gate in GATES:
            original = control_backup.read_text(encoding='utf-8')
            wrapper = f'''\n# Temporary control mutation; restored from backup by mutations.py.\n_original_document = check_document\n_original_source = source_checks\ndef check_document(*args, **kwargs):\n    return [e for e in _original_document(*args, **kwargs) if e.gate != {gate!r}]\ndef source_checks(*args, **kwargs):\n    return [e for e in _original_source(*args, **kwargs) if e.gate != {gate!r}]\n'''
            control.write_text(original + wrapper, encoding='utf-8')
            result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_gate*.py', '-v'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
            assert result.returncode != 0, f'{gate} disabled control survived tests'
            print(f'{gate} disabled control: TESTS RED (expected)')
            print(result.stdout + result.stderr)
            shutil.copyfile(control_backup, control)
            result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_gate*.py', '-v'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
            assert result.returncode == 0, result.stdout + result.stderr
            print(f'{gate} restored control: TESTS GREEN')
            print(result.stdout + result.stderr)
    finally:
        shutil.copyfile(control_backup, control)
    export = ROOT / 'scripts/facts/export.py'
    original = export.read_text(encoding='utf-8')
    prove_control(export, folder / 'export.py.backup', original.replace("if row['status'] == 'verified'", 'if True'), 'test_registry.py', 'verified-only export')
    text_helper = ROOT / 'scripts/sources/fetch_text.py'
    original = text_helper.read_text(encoding='utf-8')
    prove_control(text_helper, folder / 'fetch_text.py.backup', original.replace('"script", ', ''), 'test_registry.py', 'source script exclusion')
    built = ROOT / '.cache/test-public/playbooks/test-page/index.html'
    original = built.read_text(encoding='utf-8')
    prove_control(built, folder / 'built.html.backup', original.replace('</head>', '<script src="https://example.invalid/x.js"></script></head>'), 'test_build.py', 'built resource test')


if __name__ == '__main__':
    main()
