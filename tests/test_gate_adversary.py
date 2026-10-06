"""Concrete bypass sequences found during the local adversary pass."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/gates'))
from gates import Context, check_document


class GateAdversaryTests(unittest.TestCase):
    def setUp(self):
        self.ctx = Context.fixture()
        self.html = (ROOT / 'tests/fixtures/gates/page.html').read_text(encoding='utf-8')

    def gates(self, text):
        return {e.gate for e in check_document(text, self.ctx, require_trust=True)}

    def test_inline_tags_do_not_reset_sentence_limit(self):
        sentence = '<p>' + 'read ' * 13 + '<em>' + 'read ' * 13 + '</em>.</p>'
        self.assertIn('G10', self.gates(self.html.replace('</article>', sentence + '</article>')))

    def test_empty_signature_element_fails(self):
        self.assertIn('G3', self.gates(self.html.replace('Verified by TEST.', '')))

    def test_srcset_cannot_hide_second_external_resource(self):
        self.assertIn('G4', self.gates(self.html.replace('</article>', '<img srcset="/a.png 1x, https://example.invalid/b.png 2x"></article>')))

    def test_redirect_cannot_request_external_host(self):
        self.assertIn('G4', self.gates(self.html.replace('</head>', '<meta http-equiv="refresh" content="0; url=https://example.invalid"></head>')))

    def test_contact_marker_cannot_change_target(self):
        self.assertIn('G1', self.gates(self.html.replace('href="https://example.invalid/test"', 'href="https://example.invalid/other"')))

    def test_expired_fact_fails(self):
        self.ctx.facts['TEST-STEP-01']['recheck_by'] = '2000-01-01'
        self.assertIn('G2', self.gates(self.html))

    def test_lookalike_primary_domain_fails(self):
        self.ctx.facts['TEST-STEP-01'].update(kind='rule', source_url='https://rbi.org.in.example.invalid/rule')
        self.assertIn('G9', self.gates(self.html))

    def test_frame_privacy_prose_is_checked(self):
        self.assertIn('G10', self.gates(self.html.replace('<p data-build-commit', '<p>paisa</p><p data-build-commit')))

    def test_evidence_does_not_exempt_unreferenced_links(self):
        self.assertIn('G1', self.gates(self.html.replace('<summary>Evidence</summary>', '<summary>Evidence</summary><a href="https://example.invalid/other">Read</a>')))

    def test_only_quote_bypasses_evidence_prose_check(self):
        self.assertIn('G10', self.gates(self.html.replace('<summary>Evidence</summary>', '<summary>Evidence</summary><p>paisa</p>')))

    def test_verified_share_base_retains_exact_encoded_text(self):
        self.ctx.contacts['C99'].update(type='url-base', value='https://example.invalid/?text=')
        text = self.html.replace('href="https://example.invalid/test"', 'data-share-text="Read the test note." href="https://example.invalid/?text=Read+the+test+note."').replace('>https://example.invalid/test</a>', '>WhatsApp</a>')
        self.assertNotIn('G1', self.gates(text))
        self.assertIn('G1', self.gates(text.replace('?text=Read+', '?text=Send+')))

    def test_plain_email_and_unschemed_url_are_bare_contacts(self):
        for value in ['person@example.invalid', 'www.example.invalid', 'example.invalid/test']:
            with self.subTest(value=value):
                self.assertIn('G1', self.gates(self.html.replace('</article>', '<p>' + value + '</p></article>')))


if __name__ == '__main__':
    unittest.main()
