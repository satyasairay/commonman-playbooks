"""L03c failing fixtures, before format implementation."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/gates'))
sys.path.insert(0, str(ROOT / 'scripts/facts'))
from gates import Context, frontmatter
from formats import project
from format_gate import check_format


class FormatTests(unittest.TestCase):
    def setUp(self):
        self.ctx = Context.fixture()
        meta, body = frontmatter(ROOT / 'tests/fixtures/site/en/playbooks/test-page.md')
        self.record = project(meta, body, self.ctx, 'en', '/playbooks/test-page/')

    def test_whatsapp_baseline(self):
        text = self.record['whatsapp']
        self.assertLessEqual(len(text), 700)
        self.assertEqual(check_format('whatsapp', text, self.record, self.ctx), [])
        self.assertIn('https://example.invalid/test', text)
        self.assertIn('Read the test note.', text)

    def test_whatsapp_length_mutation(self):
        self.assertIn('G12', {e.gate for e in check_format('whatsapp', self.record['whatsapp'] + 'x' * 800, self.record, self.ctx)})

    def test_added_step_mutation(self):
        text = self.record['whatsapp'].replace('Read the test note.', 'Send the test note.')
        self.assertIn('G12', {e.gate for e in check_format('whatsapp', text, self.record, self.ctx)})

    def test_two_page_sheet_mutation(self):
        self.assertIn('G12', {e.gate for e in check_format('print', '', self.record, self.ctx, pages=2)})

    def test_missing_pdf_count_fails_closed(self):
        self.assertIn('G12', {e.gate for e in check_format('print', '', self.record, self.ctx)})

    def test_source_claim_blocks_projection(self):
        meta, _ = frontmatter(ROOT / 'tests/fixtures/site/en/playbooks/test-page.md')
        with self.assertRaises(ValueError):
            project(meta, '## Do this now\n\n1. Reply within 3 days.', self.ctx, 'en', '/playbooks/test-page/')


if __name__ == '__main__':
    unittest.main()
