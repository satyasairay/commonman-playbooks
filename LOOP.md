# LOOP.md

## Binding constraint

Trust, checked by one person. A page is right only after Satya has checked it against its sources and signed it. So the constraint is verified pages in a real reader's hands per hour of Satya's review, and it sets the order below. Work that saves Satya's review time goes early. Pages he cannot verify yet go late. One wrong phone number on a live page does more harm than no site, so the gates come before the pages.

Facts are checked once, in rules/facts.md, and every format and language is built from them. That keeps Satya's review time from growing with each new format and language.

Second priority, set by Satya: new scams get in early. The radar starts collecting in L04. The first scam card ships with the first playbook in L05.

## THE PROTOCOL (what `/next` does, every time)

1. ORIENT — read STATE.md → LOOP.md; state in one line which loop and its DONE WHEN.
2. HEALTH — check prod/live surfaces and `git status` clean. Broken prod becomes the loop.
3. GATES — if a USER DOES item precedes the work and is not done: give exact steps, mark
   `blocked:<reason>`, do the unblocked sub-steps.
4. BUILD — small commits; tests green before every push; branch + PR once CI exists.
4b. ADVERSARY — before shipping, attack your own output with independent hostile passes
   (security/data · product truth · visual for UI · operability for runbooks). Report only
   defects triggerable by a concrete sequence. Every confirmed finding becomes a failing test
   first, then a fix. Mutation-check every test guarding a control: break the control, confirm
   red, restore from a backup copy (never `git checkout`). A test that cannot fail is worse
   than no test. Cross-engine review when two model families are available — no shared blind spots.
5. SHIP — deploy and verify from OUTSIDE the box (curl, screenshots, checkers). Success is
   measured, never asserted.
6. RECORD — update STATE.md (row, decisions, known issues, next), commit, push.
7. HANDHOLD — end with: (a) what happened in plain English, (b) what to look at, (c) what the
   user must do before the next `/next` (numbered, exact commands), (d) one line on what the
   next `/next` will do.

Lanes: ROUTINE (inside the plan) — proceed and record. NOVEL (money, data deletion, emails to
real people, DNS/account settings, customer-visible legal text, prices, plan rewrites) — ask,
every time. One active loop per session; a loop is 30–150 min of work; bigger loops split
loudly, never half-finish silently.

### Project additions to the protocol

- The NOVEL lane also covers: publishing or unpublishing a page, any change to rules/contacts.md, rules/facts.md or rules/allowed-terms.md, any change on the VPS, the project name, the licence, the opening line, and any text that names a real person or organisation as a scammer.
- For content, BUILD is the pipeline in PIPELINE.md. Facts come first, in their own PR. Pages come after, and only use verified facts.
- For content, ADVERSARY has five passes: harm, truth, scam look-alike, reading, and formats. See .claude/agents/adversary.md.
- Cross-engine review is the Codex check (AGENTS.md, Job 1). Every fact and every page needs it.
- Satya may reject any draft, any number of times, with or without a reason. A rejection with a reason becomes a rule in rules/house-rules.md, section 13.
- No engine sets `draft: false`. Satya sets it, together with `verified_by` and `verified_on`, in the PR he merges.
- Commits and PR descriptions carry no `Co-Authored-By` line and no other AI credit line.

## MINIMUM USEFUL (MU)

This project has no buyer, so MINIMUM USEFUL replaces MINIMUM SELLABLE: the smallest honest product that a named reader uses.

- **Reader:** a person in Odisha whose money just left their bank account without their consent.
- **Use:** they open one link, or read one forwarded WhatsApp message, on a low-end Android phone, and do the first three steps without help.

MU contains:
- Playbook F2, "Money left my account and I didn't send it", in three formats: web page, WhatsApp text, print sheet. Signed by Satya.
- One scam card, sideloaded adult apps that drain bank accounts (I4C advisory, 26 August 2026), as a web page and WhatsApp text.
- Every fact and contact these need, verified.
- The Method page and the corrections page.
- Hard gates G1 to G12, all passing.
- Live on satsangee.org, in English.

**MU DONE WHEN:** 4 of 5 test readers who have never seen the page reach step 3 within 5 minutes without asking anyone. One of the five gets only the WhatsApp text. G1 to G12 pass when checked from outside the server.

## EXECUTION ORDER

| # | Loop | Goal | Needs first |
|---|---|---|---|
| 1 | L01 | House rules, opening line and allowed terms signed | none |
| 2 | L02 | Contacts and the first facts verified | none |
| 3 | L03a | Site skeleton, fact and contact references, trust frame | Hugo installed |
| 4 | L03b | Machine gates and CI | L03a; repo and first commit for CI |
| 5 | L03c | WhatsApp text and print formats | L03b |
| 6 | L04 | Radar v0: collect only | repo on GitHub |
| 7 | L05 | Playbook F2 and first scam card in their formats; 5-reader test | L01, L02, L03c |
| 8 | L06 | Deploy path, security.txt and takedown drill | Satya's VPS steps |
| 9 | L07 | Method page and corrections page | L01 |
| | | **MU reached** | |
| 10 | L08 | F1 (tricked into paying) and 4 cards | MU |
| 11 | L09 | F5 (threatened right now) and the digital arrest card | MU |
| 12 | L10 | F3 (phone or WhatsApp taken over) and 4 cards | MU |
| 13 | L11 | F4 (someone is using my identity) and 1 card | MU |
| 14 | L12 | F6 (clicked, shared or installed; no money lost yet) | MU |
| 15 | L12b | "What happened?" start page | L12 |
| 16 | L13 | Radar v1: signal to card PR in 24 hours | L04, L08 |
| 17 | L14 | Odia, Hindi and audio | Odia and Hindi opening lines written by Satya (deferred from L01); a human reader per language |
| 18 | L15 | Drift monitor: a changed source flags its facts and every page that uses them | L05 |
| 19 | L16 | Impersonation watch | L06 |
| 20 | L17 | Public launch | L08 to L16 |

After L17, life-event playbooks E1 to E8 (rules/taxonomy.md), ordered by what readers ask for.

## Loops

### L01 · House rules, opening line and allowed terms signed

- **GOAL:** Satya approves the rules every draft follows, the opening line in English, Odia and Hindi, and the list of allowed terms.
- **CLAUDE DOES:**
  - Offer three English versions of the opening line. For each, say where it works best and where it could go wrong.
  - Walk through rules/house-rules.md one section at a time. Record each change Satya makes.
  - Walk through rules/allowed-terms.md, including the open question on lakh and crore.
  - Write Odia and Hindi lines only if Satya asks. Mark them `machine-draft` until he rewrites them.
- **USER DOES:**
  - Pick or rewrite the English opening line.
  - Write or approve the Odia and Hindi lines himself.
  - Approve, change or cut each house rules section and each allowed term. Decide lakh and crore.
- **DONE WHEN:** rules/house-rules.md shows the opening line as `approved` in en, with a date and Satya's initials. The or and hi lines are deferred to L14 (Satya, 30 September 2026). Every house rules section is `approved` or `cut`. Every row in rules/allowed-terms.md is `approved` or removed.
- **FILES in bounds:** rules/house-rules.md, rules/allowed-terms.md, STATE.md. **Out of bounds:** everything else.
- **Estimate:** 60 min machine, 75 min Satya.

### L02 · Contacts and the first facts verified

- **GOAL:** every contact the six families need, and every fact that F2 and seed card 1 need, is checked by Satya against a primary source.
- **CLAUDE DOES:**
  - Contacts: for each row in rules/contacts.md, find the page on the owner's own domain that states the value. Record the URL and the exact quote. Mark rows with only news support as `needs-official-source`.
  - Facts: for each F2 and card 1 topic in the candidate list in rules/facts.md, find the primary source, add it to the sources table, save a snapshot, and write the fact block: statement, every condition, quote, source location. Status `candidate`.
  - Run the Claude fact check (source-checker, mode A) and hand Satya the Codex command for mode A.
- **USER DOES:**
  - Run the Codex fact check (AGENTS.md, Job 1, mode A).
  - Open each source himself, confirm each quote, and set each contact and fact to `verified` or `rejected`, with the date and his initials.
- **DONE WHEN:** every contact is `verified` or `rejected`. Every fact that F2 and card 1 need is `verified`, with a primary-domain source, a quote, all conditions and a recheck date. Both fact checks show no NOT FOUND, PARTIAL or CONTRADICTED rows for verified facts.
- **FILES in bounds:** rules/contacts.md, rules/facts.md, STATE.md.
- **Estimate:** 2 to 3 hours machine, 3 to 4 hours Satya.

### L03a · Site skeleton, fact and contact references, trust frame

- **GOAL:** a Hugo site that builds on the PC in en, or and hi, where facts and contacts come only through references, and every page carries the trust frame.
- **CLAUDE DOES:**
  - Hugo config, layouts and i18n files (opening line, no-contact line, labels). No JavaScript, no web fonts, no analytics, no forms. System fonts, one accent colour, readable at 320 pixels wide.
  - `scripts/facts/export`: turns rules/facts.md and rules/contacts.md into data files that Hugo reads. Only `verified` rows export.
  - `fact` and `contact` shortcodes. A fact shows its statement and an evidence marker. The evidence layer (source, quote, date checked, fact id) opens with the HTML `<details>` element.
  - Page layout in this order: opening line, scope, clock (from the fact ids in front matter), body, evidence, verified-by line, "checked on" and "next check by" dates, no-contact line.
  - Site footer: commit id and build date, the privacy claim, the "Report a mistake" link.
  - Stubs for /method/ and /corrections/. `static/.well-known/security.txt`.
  - `scripts/sources/fetch`: saves each source in the facts sources table to `.cache/sources/<source id>` and writes its SHA-256 back.
  - `.gitignore` (at least `public/`, `.cache/`, `resources/`, the exported data files).
- **USER DOES:** install Hugo extended: `winget install Hugo.Hugo.Extended`
- **DONE WHEN:** `hugo` builds with zero warnings. A test page with one fact and one contact shows the statement and the evidence layer with no JavaScript. A browser network log shows zero requests to other hosts.
- **Estimate:** 2 hours.

### L03b · Machine gates and CI

- **GOAL:** the gates that stop bad pages, each proven to fail when it should.
- **CLAUDE DOES:** gate scripts in Python, run the same way on the PC and in CI, for G1, G2, G3, G4, G6, G7, G8, G9 (the domain check), G10 and G11 (definitions under HARD GATES). For each, a mutation: break the control, confirm red, restore from a backup copy. Examples: add a made-up phone number to a test page (G1); type a deadline into page text instead of using a fact (G11); add "paisa" to a test page (G10). Then the CI workflow that runs them on every pull request.
- **USER DOES:** switch on branch protection for `main` in GitHub settings. Claude gives the exact steps.
- **DONE WHEN:** each gate goes red on its mutation and green after restore, with the output pasted in STATE.md. CI runs all of them on a test PR.
- **Estimate:** 2 to 2.5 hours.

### L03c · WhatsApp text and print formats

- **GOAL:** the WhatsApp text and the print sheet are built from the same page data as the web page, and G12 checks them.
- **CLAUDE DOES:** a WhatsApp text template and its `wa.me` share link; a print layout and PDF build with WeasyPrint in CI; G12 (every format passes G1, G6, G8, G10 and G11, and its own limit) with mutations: a WhatsApp text over 700 characters, a print sheet that runs to two pages, a step in a format that is not in the page.
- **DONE WHEN:** for the test page, the WhatsApp text is 700 characters or fewer and contains only referenced facts and contacts, the PDF is exactly one page, and each G12 mutation goes red, then green after restore.
- **Estimate:** 1.5 to 2 hours.

### L04 · Radar v0: collect only

- **GOAL:** a daily radar run reads the tier-1 sources in rules/sources.md and files one `scam-signal` issue per new item. It never drafts or publishes.
- **USER DOES:** choose where it runs: a Claude Code cloud routine (runs when the PC is off; needs the GitHub repo) or a local scheduled task.
- **DONE WHEN:** 7 daily runs in a row are logged. Every I4C advisory published that week appears as an issue within 24 hours. The run wrote nothing outside GitHub issues.

### L05 · Playbook F2 and the first scam card, in their formats

- **GOAL:** F2 (web, WhatsApp text, print) and seed card 1 (web, WhatsApp text) go through the full pipeline and reach Satya's merge.
- **USER DOES:** check both pages in every format. Find 5 people who have never seen the page. Watch each one use it on their own phone; give one of them only the WhatsApp text.
- **DONE WHEN:** Satya has signed both pages. Both page checks (claude and codex) show no BARE CLAIM rows. 4 of 5 test readers reach step 3 within 5 minutes without help.

### L06 · Deploy path, security.txt and takedown drill

- **GOAL:** merging to main publishes every format to satsangee.org through a deploy user that can only write the site folder.
- **USER DOES (NOVEL, VPS):** create user `cmp-deploy`, install the rrsync-restricted key, add the Caddy site file, reload Caddy. Claude writes the exact commands. Satya runs them.
- **DONE WHEN:** a curl from outside shows HTTPS, the security headers, no `Set-Cookie`, and /.well-known/security.txt. The takedown drill (RUNBOOK R1) finishes in under 10 minutes, and the time is recorded.

### L07 · Method page and corrections page

- **GOAL:** the page that explains how everything is made (families, source tiers, facts, gates, and where AI is and is not used), and the corrections log.
- **USER DOES:** a pass in his own words, using the human-pass card that comes with the draft.
- **DONE WHEN:** Satya approves both pages and they pass G1 to G12.

### L08 to L12 · The other five families

One loop for each family: F1, F5, F3, F4, F6, in that order. Facts first, in their own PR, then the playbook in web, WhatsApp text and print, then the seed cards that point to it (rules/taxonomy.md).
- **DONE WHEN (each):** Satya has verified the new facts and signed the playbook and its cards, and all checks are clean.

### L12b · "What happened?" start page

- **GOAL:** a page that asks at most three plain questions and sends the reader to the right playbook. The first question is always "Is someone threatening you, or asking you for money, right now?"
- **DONE WHEN:** 5 test readers, each given a different situation, reach the right playbook in under a minute.

### L13 · Radar v1

- **GOAL:** an official advisory becomes a draft card PR within 24 hours, with its facts PR, the gates and both Claude checks already run. Satya only reviews.
- **DONE WHEN:** 3 real signals went from issue to merged card, and the median time from issue to PR is under 24 hours.

### L14 · Odia, Hindi and audio

- **GOAL:** every live page and fact exists in or and hi, checked by a human who reads that language, and each playbook has an audio version read by a human voice.
- **USER DOES first:** write the Odia and Hindi opening lines (deferred from L01). rules/house-rules.md, section 1, records them as `approved` with a date and initials.
- **DONE WHEN:** each translation and fact statement has `verified_by` set by a human reader of that language. Each audio file is under 400 KB with its transcript on the page. Machine translation alone never goes live.

### L15 · Drift monitor

- **GOAL:** a weekly job fingerprints every source. When one changes, it opens an issue that names every fact built on it and every page and format that uses those facts.
- **DONE WHEN:** a test fixture with a changed source opens the right issue with the full list.

### L16 · Impersonation watch

- **GOAL:** a weekly search for the project name, the domain and Satya's name being used by others to ask people for money or data.
- **DONE WHEN:** the job runs 4 weeks in a row, and RUNBOOK R6 has been walked through once as a drill.

### L17 · Public launch

- **GOAL:** the repo goes public with SECURITY.md, CONTRIBUTING.md and the licence, and Satya tells his peers.
- **USER DOES (NOVEL):** final name, licence, launch date, and the announcement in his own words.
- **DONE WHEN:** the repo is public, G1 to G12 pass from outside, and the launch note is posted.

## HARD GATES (before any page goes live)

| Gate | Test | How it is checked |
|---|---|---|
| G1 | Phone numbers, URLs and emails appear only through contact references to `verified` contacts. No phone-like number or outside URL appears anywhere else. | Build script |
| G2 | Every fact a page uses is `verified` and before its recheck date. Every page with `draft: false` has `verified_by` and `verified_on`. Scam cards show a confidence label. | Build script |
| G3 | Every live page shows the verified-by line, "checked on" and "next check by" dates, and the build's commit id. The site has /method/, /corrections/ and /.well-known/security.txt. | Build script |
| G4 | Nothing is collected: no cookies, forms, third-party requests, analytics or access logs | Build script, outside curl, browser network log, Caddy file review |
| G5 | A wrong page can be pulled in under 10 minutes | Timed drill, RUNBOOK R1 |
| G6 | Every page and format says the site never calls, never asks for money and never files anything for you | Build script |
| G7 | No loop ids, internal file names, `[[VERIFY` markers or dates that Satya has not agreed on public pages | Build script |
| G8 | The approved opening line is first on every playbook, card and format, in each language | Build script |
| G9 | Every fact of kind rule, right or deadline has a source on a primary domain, and Satya has opened it | Build script (domain), PR checklist |
| G10 | English pages are pure, simple Indian English: no Hinglish, no Devanagari or Odia script, no word outside the dictionary and rules/allowed-terms.md, no sentence over 25 words | Build script |
| G11 | No bare claims: page text outside fact references has no numbers, amounts, time periods, percentages, section numbers or names of Acts, rules or circulars (step numbers exempt) | Build script, then both page checks |
| G12 | Every format passes G1, G6, G8, G10 and G11, and its own limit (WhatsApp text 700 characters; print exactly one page; audio under 400 KB) | Build script |

## KILL LIST

| Cut | Why | Revived only by |
|---|---|---|
| Chatbot that answers readers | Nyaya Setu already does legal Q&A. A wrong AI answer to a person in panic causes harm. | Never for advice. Maybe search-only, if readers cannot find pages. |
| Accounts, forms, case tracking | Victim data makes the site a target and brings DPDP duties. The site collects nothing. | Never. |
| Filing complaints for readers | Looks exactly like the fake "recovery agents" that prey on victims. | Never. |
| Donations or any money | Satya's rule: non-profit, no income. | Satya's written decision. |
| Analytics and trackers | Privacy, and G4. | Satya's decision, and only as counts without IP addresses. |
| AI voice for audio | Voice cloning is one of the scams the site warns about. | Never. |
| QR codes on sheets for public walls | A sticker over the code sends people to a fake page. | Never on public sheets. Allowed on handouts, with the address printed beside it. |
| Share images | Needs design work, and people can forward the WhatsApp text instead. | After L17, if readers ask. |
| Mobile app | A static site on 2G works on every phone. | Test readers who cannot use the site. |
| State notes beyond Odisha | Satya can verify Odisha himself. | A reader from another state reports a gap. |
| Life-event playbooks before L17 | Scam families are more urgent and the radar feeds them. | Readers ask for one, or L17 is done. |
| Comments, forum, community | Moderation load, and scammers would use it. | Never on the site. |
| CONTRIBUTING and outside contributors | The repo is private until launch. | L17. |
| ChatGPT in CI | Needs a paid API key. | Satya decides to pay. |
| Name, logo, brand work | Placeholder name for now. | Satya picks the name (inbox 1). |
| SEO work | Nothing to rank before MU. | After MU. |

## THE DATES

Machine time is short. Human lead time sets the dates. All dates are proposals until Satya accepts them.

| Item | Machine time | Human lead time | Proposed date |
|---|---|---|---|
| L01 house rules, opening line, allowed terms | 60 min | Satya 75 min | 3 Oct 2026 |
| L02 contacts and first facts | 2 to 3 hours | Satya 3 to 4 hours | 4 Oct 2026 |
| First commit and GitHub repo | none | Satya 10 min | 3 Oct 2026 |
| L03a to L03c site, gates, formats | 5.5 to 6.5 hours | Hugo install, 5 min | 6 Oct 2026 |
| L04 radar v0 | 2 hours, then 7 days of runs | none | runs from 6 Oct, done 13 Oct 2026 |
| L05 F2 and first card | 3 hours | Satya 3 hours; 5 readers, one afternoon | 12 Oct 2026 |
| L06 deploy path | 1 hour | Satya 30 min on the VPS | 12 Oct 2026 |
| L07 Method and corrections pages | 1.5 hours | Satya 1 hour own-hand pass | 14 Oct 2026 |
| MU live | | | 17 Oct 2026 |
| L08 to L12 | about 3 hours each | Satya 3 to 4 hours each | one a week, to 21 Nov 2026 |
| L12b start page | 1.5 hours | 5 readers | 25 Nov 2026 |
| L13 radar v1 | 3 hours | none | 28 Nov 2026 |
| L14 Odia, Hindi, audio | 1 hour per page | a human reader per language, a quiet room for recording: not known yet | rolling from Nov 2026 |
| L17 public launch | 2 hours | name, domain (registrar minutes, DNS up to 48 hours), licence | 9 Dec 2026 |

## DIFFERENTIATION

What a reader would say:
- "1930 and cybercrime.gov.in take my complaint. This page told me what to do first, what to keep, and where to go when the bank said no."
- "Nyaya Setu answers my question. This page gave me the steps in order, with the deadline for each."
- "My son forwarded me the WhatsApp message, and the sheet at the bank said the same thing."
- "The law-firm blog wanted me to call their number. This page asked me for nothing and gave only official numbers."
- "It said nobody from the site will ever call me. So when someone did, I knew."

What a security peer would say:
- "Every fact has a primary source, a quote and a date one tap away, and a named person signed it."
- "The same checked facts feed the web page, the WhatsApp text and the print sheet, so they cannot disagree."
- "The scam cards come from a radar that reads I4C and police advisories every day, and they carry confidence labels like threat intel."
- "They publish their own corrections."
