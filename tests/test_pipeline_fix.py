"""Build separation, mutation isolation and CI supply-chain regressions."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class PipelineFixTests(unittest.TestCase):
    def test_S10_clean_production_and_separate_preview(self):
        text = (ROOT / 'scripts/gates/verify.py').read_text(encoding='utf-8')
        self.assertIn("'--cleanDestinationDir'", text)
        self.assertIn("'.cache/preview-public'", text)
        self.assertIn("'production-build'", text)
        self.assertIn("'--production'", text)

    def test_S13_mutations_only_in_copies(self):
        for name in ('mutations.py', 'format_mutations.py'):
            file = ROOT / 'scripts/gates' / name
            if file.exists():
                text = file.read_text(encoding='utf-8')
                self.assertIn('TemporaryDirectory', text)
                self.assertNotIn("control = ROOT / 'scripts", text)

    def test_local_format_check_is_explicit(self):
        self.assertIn('G12 NOT RUN', (ROOT / 'scripts/gates/verify.py').read_text(encoding='utf-8'))

    def test_ci_immutable_dependencies(self):
        text = (ROOT / '.github/workflows/gates.yml').read_text(encoding='utf-8')
        uses = re.findall(r'uses: ([^\s]+)', text)
        self.assertTrue(uses)
        for use in uses:
            self.assertRegex(use, r'@[0-9a-f]{40}$')
        self.assertIn('persist-credentials: false', text)
        self.assertRegex(text, r'[0-9a-f]{64}  \$archive')
        if 'pip install' in text:
            self.assertIn('--require-hashes', text)


if __name__ == '__main__':
    unittest.main()
