"""L03c CI entry point; author PDFs, check all formats and mutate artefacts."""
import os
import sys
from verify import ROOT, command


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    env = dict(os.environ)
    command([sys.executable, 'scripts/facts/build_pdfs.py', '--public', '.cache/test-public', '--public', 'public', '--public', '.cache/preview-public'], 'formats', env)
    command([sys.executable, 'scripts/gates/format_gate.py'], 'format-gates', env)
    command([sys.executable, 'scripts/gates/format_gate.py', '--production', '--content', 'content', '--public', 'public', '--facts', 'rules/facts.md', '--contacts', 'rules/contacts.md'], 'real-format-gates', env)
    command([sys.executable, 'scripts/gates/format_gate.py', '--content', 'content', '--public', '.cache/preview-public', '--facts', 'rules/facts.md', '--contacts', 'rules/contacts.md'], 'preview-format-gates', env)
    command([sys.executable, '-B', 'scripts/gates/format_mutations.py'], 'format-mutations', env)


if __name__ == '__main__':
    main()
