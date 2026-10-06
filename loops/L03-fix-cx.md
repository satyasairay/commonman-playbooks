LOOP CARD
LOOP id: L03-fix-cx (fix round for PRs #2, #3 and #4)
ENGINE: Codex CLI, model gpt-6.1-sol, reasoning high. Claude reviews again after this round.
GOAL: Fix every blocker and should-fix item in loops/L03-review.md, and the minor items listed below, on the existing branches loop/L03a-cx, loop/L03b-cx and loop/L03c-cx.
READ FIRST: loops/L03-review.md (the fix list), loops/L03-cx.md (the first card: bounds, forbidden, decisions), AGENTS.md, LOOP.md (HARD GATES), rules/house-rules.md, rules/formats.md. Read loops/ files from origin/main with git show.
WORK IN: C:\Users\USER\Desktop\commonman-playbooks-cx. First: git fetch, then bring each local loop branch up to origin with git merge --ff-only (Claude added UTF-8 re-encode commits).
BRANCH RULE: Fix each item on the lowest branch that owns the code (site and export: L03a; gates, verify and CI: L03b; formats and G12: L03c). When a branch's fixes are done, merge it into the next branch up with git merge (no rebase, no force-push), then push all three. Keep the three PRs; do not open new ones.
FILES in bounds: the same as loops/L03-cx.md.
FILES out of bounds (read only): the same as loops/L03-cx.md. Also do not change any reader-visible wording in i18n/en.toml, except to add new labels the fixes need (mark each new one "DRAFT: Satya approves").
DONE WHEN:
  - Every blocker (B1, B2) and should-fix item (S1 to S22) in loops/L03-review.md is fixed, and each has a test that failed before the fix and passes after it. Paste the red and green output in the PR that owns the fix.
  - Every reproducer named in the review (for example "1930. Call this number", "fifty per cent", "bank-refund.online", "[[ VERIFY", "<style>@import url(https://...)") is a committed test case that is now RED.
  - Each control listed in S12 has its own test, and breaking that control alone turns at least one test red.
  - CI is green on all three PRs, and verify.py exits 0 locally.
DECIDED FOR YOU (list each one in the PR that owns it, so that Satya can change it):
  - S10: the production build is hugo --cleanDestinationDir with no drafts, into public/. Previews and the TEST site build into .cache/. Gates run on both builds. G3's site-level pages (/method/, /corrections/, security.txt) are required only when the production build has at least one live playbook or card.
  - S16: disableLanguages = ['or', 'hi'] until L14.
  - S18: dates on pages read "6 October 2026"; the commit id is the first 7 characters.
  - S22: G2 accepts YYYY-MM-DD and "6 October 2026". Any other value fails with a message that names both accepted forms.
  - S14: the card label reads "Confirmed by {agency} on {date}", taken from the card's advisory fact.
  - Minor items in scope: print address 18 pt or larger; card label directly under the opening line; formats nav above the trust section; G12 requires contact C01 in the WhatsApp text and fails on words in capital letters; web page size under 50 KB checked; fact text counted in G10 sentence length; G12 print compares the whole visible sheet and rejects transform, zoom and small; G6 anchored to an approved text, read from rules/house-rules.md if a no-contact row exists there, else from i18n with a note in the PR; G11 matches "Act" and "Acts" with a capital only; verify.py prints "G12 NOT RUN" when WeasyPrint is absent; gate mutations also run on the Hugo-built TEST page; a signed TEST fixture page (draft false only inside tests/fixtures) renders the exact verified-by line; a page-level recheck_by for pages without facts; G3 requires a footer AI-line element on live pages (empty until Satya writes the text); export.py refuses fixture inputs with the default output; source ids must match src-[a-z0-9-]+ and a redirect to http fails; hugo.toml [privacy] disables and [security.http] urls = ['none']; actions pinned by full SHA, Hugo SHA-256 hardcoded, pip install with --require-hashes, persist-credentials: false; local paths redacted from evidence logs; stale docstring path fixed.
  - Out of scope (Satya decides): all reader wording, evidence source links, private vulnerability reporting, branch protection, anything in rules/.
FORBIDDEN: everything in loops/L03-cx.md FORBIDDEN. Also:
  - Write every file as UTF-8 without BOM. Do not use PowerShell >, Out-File, Set-Content or Add-Content to write files. Use your patch tool, or Python with encoding="utf-8".
  - Do not run mutations on tracked files in place. Mutate copies in a temporary folder.
  - Do not weaken a gate to make a test pass. If a fix would block a real page that the spec allows, stop that item and record why.
IF BLOCKED: as in loops/L03-cx.md. Do not stop to ask. Satya is away.
HANDOFF evidence: In each PR, a comment headed "FIX ROUND (codex)": a table of review id, file:line changed, test name, red output, green output. Last message: what is done, what is not done, each decision you made, each block with its real cause, and the commit ids pushed to each branch.
STOP: when DONE WHEN is met, or when every remaining item needs Satya. Do not start another loop.
