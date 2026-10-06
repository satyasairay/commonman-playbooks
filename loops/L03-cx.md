LOOP CARD
LOOP id: L03-cx (L03a, then L03b, then L03c, in one run)
ENGINE: Codex CLI, model gpt-6.1-sol, reasoning high. Claude reviews each PR.
GOAL: Build the site skeleton, the machine gates with CI, and the WhatsApp and print formats, as LOOP.md sections L03a, L03b and L03c say.
READ FIRST: AGENTS.md; LOOP.md (L03a to L03c, HARD GATES); PIPELINE.md (repo layout); rules/house-rules.md; rules/formats.md; rules/facts.md (references, Sources); rules/contacts.md; rules/allowed-terms.md.
WORK IN: C:\Users\USER\Desktop\commonman-playbooks-cx (your own clone). Branches: loop/L03a-cx from origin/main; loop/L03b-cx from loop/L03a-cx; loop/L03c-cx from loop/L03b-cx. One PR for each branch. Base: main for L03a, the branch before it for L03b and L03c.
FILES in bounds: hugo.toml, layouts/, i18n/, static/, content/en/ (test pages only, draft: true), scripts/facts/, scripts/gates/, scripts/sources/, tests/, .github/workflows/, .gitignore.
FILES out of bounds (read only): CLAUDE.md, STATE.md, LOOP.md, AGENTS.md, PIPELINE.md, RUNBOOK.md, README.md, rules/, archetypes/, .claude/, loops/.
DONE WHEN:
  L03a: `hugo` builds with zero warnings. A test page with one fact and one contact shows the statement and the evidence layer (HTML details element, no JavaScript). The built HTML loads nothing from another host.
  L03b: Python gates G1, G2, G3, G4, G6, G7, G8, G9 (domain check), G10 and G11 run the same way on the PC and in CI. Each gate goes red on its mutation and green after you restore from a backup copy. The red and green output is in the PR. A GitHub Actions workflow runs all gates on every PR, and it ran on the L03b PR.
  L03c: For the test page, the WhatsApp text is 700 characters or fewer and holds only referenced facts and contacts. The print PDF (WeasyPrint, built in CI) is exactly one page. G12 goes red on each mutation (text over 700 characters, a two-page sheet, a step that is not in the page) and green after restore.
TESTS FIRST: Write each failing fixture before its gate. G1: a made-up phone number. G2: a fact that is not verified. G3: no verified-by line. G4: a script tag and an outside URL. G6: no no-contact line. G7: a [[VERIFY marker. G8: no opening line. G9: a rule fact on a news domain. G10: "paisa", and a 26-word sentence. G11: a deadline typed as text. G12: the three L03c mutations.
DECIDED FOR YOU (list each one in the PR, so that Satya can change it):
  - Tests use copies in tests/fixtures/, with one fake fact and one fake contact marked TEST and verified. Do not change the real rows in rules/.
  - Export reads rules/facts.md and rules/contacts.md and exports only verified rows. Main has no verified rows yet, so the real site has no fact text yet. That is correct.
  - Port C:\Users\USER\Desktop\commonman-playbooks\.cache\tools\fetch_text.py to scripts/sources/, and check_quotes.py to scripts/facts/. Keep their text rules, so that the saved sources and their SHA-256 values stay valid.
  - G10 does not check the verbatim quotes in the evidence layer (STATE.md, known issue K13). Word list: an en_GB list with a free licence, committed with its licence, plus rules/allowed-terms.md.
  - i18n: the English opening line comes from rules/house-rules.md, section 1. The or and hi entries stay empty (deferred to L14). G8 checks only languages that have pages.
  - No-contact line, footer privacy claim and labels: write drafts in i18n/en and mark each one "DRAFT: Satya approves" in the PR. "Report a mistake" links to /corrections/.
  - security.txt Contact: https://github.com/satyasairay/commonman-playbooks/security/advisories/new. Say in the PR that Satya must switch on private vulnerability reporting.
FORBIDDEN:
  - Do not merge, push to main or force-push. Do not touch the VPS, secrets, GitHub settings or branch protection.
  - Do not set verified, draft: false, verified_by or verified_on. Do not edit rules/.
  - No JavaScript, web fonts, CDNs, analytics, cookies, forms or third-party requests in the site.
  - No Co-Authored-By line or other AI credit line in commits or PR text. Commit with the clone's local git identity. Do not change it.
  - Gates use the Python standard library only. WeasyPrint is used only in the L03c CI job.
  - Do not get around a CAPTCHA, a login or a bot check when you fetch anything.
  - Windows: keep each shell command under 7,500 characters. Do not write a whole file with a heredoc. Put code that has backslashes in a file. Use Bash syntax only in Bash and PowerShell syntax only in PowerShell. If a command fails, name the real cause.
IF BLOCKED: If a push or a PR fails, continue and commit locally, and list the unpushed branches at the end. Do not try other ways to log in. If one gate cannot be finished, write down why and continue with the others. Do not stop to ask. Satya is away.
HANDOFF evidence: In each PR: this card, the hugo build output, the test and gate output, the red and green output for each mutation, the HTML of the test page, the WhatsApp character count and the PDF page count. Last message: what is done, what is not done, each decision you made, each branch and PR link, and each block with its real cause.
STOP: when the L03c DONE WHEN is met, or when every step that remains needs Satya. Do not start another loop.
