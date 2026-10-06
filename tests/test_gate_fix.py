"""Each reviewed bypass and each independently breakable control has a test."""
import copy
import datetime as dt
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/gates'))
from gates import Context, check_document, source_checks, run
from english import errors as english_errors
import registry

NUMBER_TIME_LEGAL = (
    'within a few days', 'in a week', 'for a year', 'golden hour',
    'in a fortnight', 'fifty days', 'zero liability', 'fifty per cent',
    'fifty rupees', 'half of the money', 'before the end of March',
    'on the same day', 'Code of Criminal Procedure', 'Integrated Ombudsman Scheme',
    'Master Direction', 'RBI circulars', 'An RBI rule', 'SEBI Regulations',
    'Both Acts', 'the Sections', 'within three working days', 'in 5 days',
    '90-day', '₹25,000', 'Rs. 5000', 'section 173', 'Limitation Act',
    'forty days', 'seventy days', 'eighty days', 'dozen days', 'several weeks',
    'couple of hours', 'ten percent', 'Sanhita', 'Adhiniyam', 'Ordinances', 'notifications',
)

class FixGateTests(unittest.TestCase):
    def setUp(self):
        self.ctx = Context.fixture()
        self.ctx.today = dt.date(2026, 10, 6)
        self.html = (ROOT / '.cache/test-public/playbooks/test-page/index.html').read_text(encoding='utf-8')

    def source(self, body, meta=None):
        return source_checks(meta or {'draft': True, 'kind': 'playbook'}, body, self.ctx)

    def document(self, addition='', **kwargs):
        return check_document(self.html.replace('</article>', addition + '</article>'), self.ctx, **kwargs)

    def assertGate(self, gate, errors):
        self.assertIn(gate, {e.gate for e in errors}, '\n'.join(map(str, errors)))

    def test_B1_only_sequential_steps_exempt(self):
        for body in ('1930. Call this number first if money left your account.', '155260) Call this number.', '999999999. Call this number.', '1. Read.\n3. Read.'):
            with self.subTest(body=body):
                self.assertGate('G11', self.source(body))
        self.assertFalse([e for e in self.source('1. Read.\n2. Read.\n3. Read.') if e.gate in {'G1', 'G11'}])

    def test_B1_built_ol_start(self):
        for start in (1930, 155260, 999999999):
            with self.subTest(start=start):
                errors = self.document(f'<ol start="{start}"><li>Call this number.</li></ol>')
                self.assertGate('G1', errors)
                self.assertGate('G11', errors)

    def test_B2_all_review_claims(self):
        for body in NUMBER_TIME_LEGAL:
            with self.subTest(body=body):
                self.assertGate('G11', self.source(body))
                self.assertGate('G11', self.document('<p>' + body + '</p>'))

    def test_G11_lowercase_act_heading_allowed(self):
        self.assertFalse([e for e in self.source("If they don't act") if e.gate == 'G11'])

    def test_G11_modal_may_is_not_a_month(self):
        self.assertFalse([e for e in self.source('You may read the note.') if e.gate == 'G11'])

    def test_S1_hard_wrap_does_not_end_sentence(self):
        text = 'Read ' + 'the note ' * 8 + '\n' + 'the note ' * 8 + '.'
        self.assertTrue(any('sentence' in e for e in english_errors(text, self.ctx.allowed_words)))

    def test_S2_deny_and_phrase_names(self):
        for word in ('didi', 'saathi', 'nyaya', 'beta', 'bas', 'na', 'paisa', 'karein', 'jaldi', 'ji'):
            with self.subTest(word=word):
                self.assertTrue(english_errors(word, self.ctx.allowed_words))
        for name in ('Sanchar Saathi', 'Nyaya Setu', 'Samadhan Didi', 'Tele-Law', 'CRIF High Mark', 'Rath Yatra'):
            with self.subTest(name=name):
                self.assertEqual(english_errors(name, self.ctx.allowed_words), [])

    def test_S3_domains_and_obfuscated_email(self):
        for body in ('bank-refund.online', 'kyc-update.top', 'bank-help.app', 'help [at] bank [dot] co', 'help (at) bank (dot) co'):
            with self.subTest(body=body):
                self.assertGate('G1', self.source(body))
                self.assertGate('G1', self.document('<p>' + body + '</p>'))

    def test_S4_raw_internal_markers(self):
        for body in ('[[ VERIFY', '[[verify', '[VERIFY', '<!-- [[ VERIFY -->', 'facts.md', 'contacts.md'):
            with self.subTest(body=body):
                self.assertGate('G7', self.source(body))

    def test_S5_kind_closed_in_sections(self):
        for kind in (None, 'Playbook', 'scam-card'):
            with self.subTest(kind=kind):
                self.assertGate('G8', self.run_site(kind=kind))

    def run_site(self, kind='playbook', suffix='.md', live=False, production=False, omit=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content, public = root / 'content', root / 'public'
            source = content / ('en/playbooks/page' + suffix)
            source.parent.mkdir(parents=True)
            meta = "+++\ntitle = 'Test page'\ndraft = " + ('false' if live else 'true') + '\n'
            if kind is not None:
                meta += f"kind = '{kind}'\n"
            if live:
                meta += "verified_by = 'TEST'\nverified_on = '2026-10-06'\nrecheck_by = '2099-01-01'\n"
            source.write_text(meta + '+++\nRead the test note.', encoding='utf-8')
            page = public / 'playbooks/page/index.html'
            page.parent.mkdir(parents=True)
            if omit != 'live':
                page.write_text(self.html, encoding='utf-8')
            for name in ('method/index.html', 'corrections/index.html', '.well-known/security.txt'):
                if name != omit:
                    file = public / name
                    file.parent.mkdir(parents=True, exist_ok=True)
                    file.write_text(self.html if name.endswith('.html') else 'TEST', encoding='utf-8')
            return run(content, public, self.ctx, production=production)

    def test_S6_non_md_content_fails(self):
        self.assertGate('G2', self.run_site(suffix='.markdown', live=True))

    def test_S7_unknown_fact_kind_fails(self):
        for kind in ('Rule', 'deadline (RBI circular)'):
            self.ctx.facts['TEST-STEP-01'].update(kind=kind, source_url='https://news.example.invalid/rule')
            self.assertGate('G9', self.document())

    def test_S8_quote_keeps_marker_contact_script_checks(self):
        for body, gate in (('[[ VERIFY', 'G7'), ('पैसा', 'G10'), ('Call 1930', 'G1')):
            html = self.html.replace('<blockquote>Read the test note.</blockquote>', '<blockquote>' + body + '</blockquote>')
            self.assertGate(gate, check_document(html, self.ctx))

    def test_S8_verified_by_is_checked(self):
        meta = {'kind': 'playbook', 'draft': False, 'verified_on': '2026-10-06', 'verified_by': 'Satyasai Ray. Paisa gone? Call 1930 ... [[VERIFY'}
        errors = self.source('', meta)
        for gate in ('G1', 'G7', 'G10'):
            self.assertGate(gate, errors)
        html = self.html.replace('Draft awaiting review', meta['verified_by']).replace('data-draft', 'data-verified-by')
        for gate in ('G1', 'G7', 'G10'):
            self.assertGate(gate, check_document(html, self.ctx))

    def test_S9_every_network_surface(self):
        for markup in ('<style>@import url(https://example.invalid/x)</style>', '<style>@font-face{src:url(https://example.invalid/x)}</style>', '<a href="/" ping="https://example.invalid/x">Read</a>', '<body background="https://example.invalid/x">', '<svg><image xlink:href="https://example.invalid/x"></svg>'):
            with self.subTest(markup=markup):
                self.assertGate('G4', self.document(markup))

    def test_S10_production_rejects_draft_output(self):
        self.assertGate('G3', self.run_site(production=True))

    def test_S11_valid_build_identity_required(self):
        for value in ('', 'TEST', 'zzzzzzz'):
            html = self.html.replace('abcdef0123456789abcdef0123456789abcdef01', value)
            self.assertTrue(any('build commit must' in e.note for e in check_document(html, self.ctx, require_trust=True)))
        html = self.html.replace('data-build-date="2026-10-06"', 'data-build-date="not a date"')
        self.assertTrue(any('invalid build date' in e.note for e in check_document(html, self.ctx, require_trust=True)))

    def test_S12_primary_https_control(self):
        self.ctx.facts['TEST-STEP-01'].update(kind='rule', source_url='http://rbi.org.in/rule')
        self.assertGate('G9', self.document())

    def test_S12_primary_username_control(self):
        self.ctx.facts['TEST-STEP-01'].update(kind='rule', source_url='https://reader@rbi.org.in/rule')
        self.assertGate('G9', self.document())

    def test_S12_live_signature_control(self):
        self.assertGate('G2', self.source('Read.', {'draft': False, 'kind': 'playbook'}))

    def test_S12_recheck_boundary_control(self):
        self.ctx.facts['TEST-STEP-01']['recheck_by'] = self.ctx.today.isoformat()
        self.assertGate('G2', self.document())

    def test_S12_card_confidence_control(self):
        self.assertGate('G2', self.source('Read.', {'draft': True, 'kind': 'card'}))

    def test_S12_required_site_pages_control(self):
        for name in ('method/index.html', 'corrections/index.html', '.well-known/security.txt'):
            with self.subTest(name=name):
                self.assertTrue(any(name in e.note and e.gate == 'G3' for e in self.run_site(live=True, omit=name)))

    def test_S12_live_page_missing_control(self):
        self.assertTrue(any('live page missing' in e.note for e in self.run_site(live=True, omit='live')))

    def test_S12_loop_id_control(self):
        self.assertGate('G7', self.source('L03-cx'))

    def test_S12_internal_path_control(self):
        self.assertGate('G7', self.source('scripts/gates/check'))

    def test_S12_call_short_phone_control(self):
        self.assertGate('G1', self.source('Call 1930'))

    def test_S22_two_date_forms_only(self):
        self.assertEqual(registry.parse_date('2026-10-06'), dt.date(2026, 10, 6))
        self.assertEqual(registry.parse_date('6 October 2026'), dt.date(2026, 10, 6))
        for value in ('30 Sep 2026', '90 days after verification', '2026/10/06'):
            with self.assertRaisesRegex(ValueError, 'YYYY-MM-DD.*6 October 2026'):
                registry.parse_date(value)

    def test_fact_sentence_counts_in_G10(self):
        statement = 'Read ' + 'the note ' * 6
        self.ctx.facts['TEST-STEP-01']['statements']['en'] = statement
        html = self.html.replace('data-fact="TEST-STEP-01">Read the test note.</span>', 'data-fact="TEST-STEP-01">' + statement + '</span><em>' + 'the note ' * 7 + '.</em>')
        self.assertGate('G10', check_document(html, self.ctx))

    def test_footer_ai_line_required(self):
        self.assertTrue(any('AI-line element' in e.note for e in check_document(self.html.replace('data-ai-line', 'data-removed'), self.ctx, require_trust=True)))

    def test_web_size_limit(self):
        self.assertGate('G12', check_document(self.html + '<!--' + 'x' * 50000 + '-->', self.ctx))


if __name__ == '__main__':
    unittest.main()
