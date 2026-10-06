"""Failing fixtures were committed before the gate implementation."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/gates'))
from gates import Context, check_document, source_checks


class GateTests(unittest.TestCase):
    def setUp(self):
        self.ctx = Context.fixture()
        self.html = (ROOT / 'tests/fixtures/gates/page.html').read_text(encoding='utf-8')

    def test_baseline(self):
        self.assertEqual(check_document(self.html, self.ctx, require_trust=True), [])

    def test_each_failing_fixture(self):
        mutations = json.loads((ROOT / 'tests/fixtures/gates/mutations.json').read_text())
        for item in mutations:
            with self.subTest(gate=item['gate'], mutation=item):
                ctx, html = copy.deepcopy(self.ctx), self.html
                if item['target'] == 'html':
                    self.assertIn(item['old'], html)
                    html = html.replace(item['old'], item['new'])
                else:
                    ctx.facts['TEST-STEP-01'][item['field']] = item['new']
                    if 'kind' in item:
                        ctx.facts['TEST-STEP-01']['kind'] = item['kind']
                self.assertIn(item['gate'], {e.gate for e in check_document(html, ctx, require_trust=True)})

    def test_raw_source_claim_is_checked_even_when_hugo_omits_html(self):
        errors = source_checks({'draft': True, 'kind': 'playbook'}, '<script src="https://example.invalid/x"></script>\nReply in three days.', self.ctx)
        self.assertTrue({'G1', 'G4', 'G11'} <= {e.gate for e in errors})


if __name__ == '__main__':
    unittest.main()
