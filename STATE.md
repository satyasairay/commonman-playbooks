# STATE.md

Loop memory. Facts only. Updated at the end of every session. Only the main Claude session edits this file.

## Where we are

**29 Sep 2026.** Spine created in D:\commonman-playbooks. Working name: Commonman Playbooks (placeholder). Empty git repo on branch `main`, no commit yet. Satya decides the first commit (see "First commit" below). No site, no content and no code exist yet. All contacts in rules/contacts.md are unverified.

Later the same day, Satya approved the plan change: a facts registry (rules/facts.md), formats (rules/formats.md) with trust signals, and gates G11 (no bare claims) and G12 (formats). L03 is now L03a to L03c. Nothing is verified yet.

**30 Sep 2026.** L01 mostly done. Satya approved the English opening line, house rules sections 2 to 11, the byline (name and date only), and every allowed term, including lakh and crore. The repo goes public right after the first commit. Still open for L01: the Odia and Hindi opening lines, and the AI line in Satya's own words. Hugo and Codex are installed on the PC. First commit made and pushed to the public repo `satyasairay/commonman-playbooks`, so work can continue on another PC.

Later on 30 Sep 2026, work moved to a second PC (no D: drive; the clone is in the Desktop folder). On that PC, Satya installed gh, Hugo extended and Codex CLI, and signed in to gh and to Codex with ChatGPT. Satya deferred the Odia and Hindi opening lines to L14. Claude proposed wording for the AI line (inbox 4); it waits for Satya's yes or rewrite. L02 started.

L02, same day: research found the sources and quotes for 18 contacts (3 of them new: C19 to C21) and drafted 62 candidate facts in five groups: RBI liability rules from 1 January 2027 (31), RBI Ombudsman Scheme 2026 (10), reporting and the Money Restoration Module (12), Zero FIR (6), and seed card 1 (3). The Claude fact check found 27 PARTIAL rows (statements a little wider than their quotes, or missing conditions) and no CONTRADICTED or NOT FOUND rows; all 27 were fixed before the PR. All 24 sources are saved in `.cache/sources/` on the second PC only (not committed; excluded through `.git/info/exclude` until L03a adds `.gitignore`). A script checked every quote against its saved copy: 0 missing, and the script was mutation-checked. Three findings change the plan: the 2017 RBI liability circular is withdrawn and its text now sits in the 2025 Directions; new liability rules apply to transactions from 1 January 2027; and the 2021 Ombudsman Scheme was replaced on 1 July 2026. Fact PR opened: https://github.com/satyasairay/commonman-playbooks/pull/1 (branch `draft/fact-f2-and-contacts`). Waiting for Satya: the decisions in inbox 12 to 15, the RBI PDF download (user to-do), the Codex check, and his verification.

## Loop status

| Loop | Goal | Status | Date | Commit |
|---|---|---|---|---|
| L00 | Spine: CLAUDE, STATE, LOOP, AGENTS, PIPELINE, RUNBOOK, README, rules, templates, agent roles | done | 29 Sep 2026 | first commit |
| L00b | Plan change: facts registry, formats, trust signals, gates G11 and G12 | done | 29 Sep 2026 | first commit |
| L01 | House rules, opening line and allowed terms signed | in progress: only the AI line is open (Claude's proposed wording waits for Satya). Odia and Hindi lines deferred to L14. | 30 Sep 2026 | |
| L02 | Contacts and the first facts verified | in progress: fact PR open; waiting for Satya (inbox 12 to 15, RBI PDF, Codex check, verification) | 30 Sep 2026 | |
| L03a | Site skeleton, fact and contact references, trust frame | pending | | |
| L03b | Machine gates and CI | pending | | |
| L03c | WhatsApp text and print formats | pending | | |
| L04 | Radar v0: collect only | pending | | |
| L05 | Playbook F2 and first scam card in their formats; 5-reader test | pending | | |
| L06 | Deploy path, security.txt and takedown drill | blocked: Satya's VPS steps | | |
| L07 | Method page and corrections page | pending | | |
| L08 to L17 | See LOOP.md | pending | | |

## Production facts

- **Domain:** satsangee.org. DNS at Hostinger (ns1 and ns2.dns-parking.com). The A record points to the VPS, TTL 60. No HTTPS yet: Caddy has no site for this domain (checked 29 Sep 2026). Checked again from outside on 30 Sep 2026: HTTP returns Caddy's default "VPS host ready" text with status 200; the HTTPS handshake fails.
- **Server:** a VPS running Caddy. Its hardware, software and access details are kept outside this public repo. Claude access is read-only.
- **Secrets:** SSH keys on Satya's PC. No other secrets exist yet. Planned: GitHub Actions secrets `DEPLOY_SSH_KEY` and `DEPLOY_KNOWN_HOSTS` (L06).
- **GitHub:** `satyasairay/commonman-playbooks`, public from the first commit (30 Sep 2026). Commits use the GitHub no-reply address, never a personal email: each clone sets `user.email` to `79207792+satyasairay@users.noreply.github.com` in its local git config.
- **Engines:** Claude Code (Max 20x) is the main engine. Codex CLI signed in with ChatGPT Pro is the second engine for fact and page checks. Codex runs on the PC only.

## User inbox

1. **NOVEL. Project name.** Placeholder: Commonman Playbooks. Research on 29 Sep 2026:
   - Rejected: *Satsangee*, the established name of the devotee community of Sree Sree Thakur Anukulchandra's Satsang (over 2,000 branches). *Dhairya*: several NGOs, and the .org, .in and .com domains are all taken. *Agla Kadam*: aglakadam.co.in already publishes help with welfare schemes.
   - Still open: *Ab Kya Karein*, *Pehle Yeh*, *Ab Aage*. None of their .org, .in or .com domains had DNS records on 29 Sep 2026. That is a signal only; confirm at a registrar.
2. **NOVEL. Temporary host.** Readers may think a site on satsangee.org belongs to Satsang. Proposal: move and 301-redirect when the real name's domain exists, at L17 at the latest.
3. ~~First commit.~~ Made and pushed 30 Sep 2026, on Satya's instruction.
4. **Opening line and AI line (L01).** English opening line approved 30 Sep 2026: "Don't worry. What happened is not in your hands now. What you do next is in your hands." Odia and Hindi lines deferred to L14 (Satya, 30 Sep 2026). **Still needed: the AI line** for the Method page and footer (house rules, section 12). Claude's proposed wording, from how the work is done today: "AI tools draft these pages and check each claim against its source. Satyasai Ray checks every fact against the official source and signs every page." Say yes or rewrite it. If it stays, "AI" and "Satyasai Ray" need rows in rules/allowed-terms.md for G10 (the byline needs the name row too).
5. **Site generator.** Hugo (decision log). Veto if you want another.
6. ~~Byline.~~ Decided 30 Sep 2026: name and date only; the 14 years goes on the Method page once.
7. **Licence (L17, NOVEL).** Proposal: content CC BY-SA 4.0, code MIT.
8. **External deadline.** None recorded. Confirm there is none.
9. ~~When the repo goes public.~~ Decided 30 Sep 2026: right after the first commit.
10. ~~Plan change: one set of facts, many formats.~~ Approved 29 Sep 2026 and written in (decisions log).
11. ~~Lakh and crore.~~ Decided 30 Sep 2026: allowed.
12. **NOVEL. F2 and the RBI rule change on 1 January 2027.** Transactions before that date follow the old liability rules (report within 3 working days, fixed limits, credit back within 10 working days). Transactions from that date follow the new rules (report within 5 calendar days, the bank's policy after that, and a small-value compensation of 85% of the net loss or ₹25,000 when the reader was careless). F2 will go live before the switch, so a reader in October to December needs the old rules. Proposal: F2 carries both sets from the start, and the page asks the reader when the money left. Other options: old rules only now and the new rules in December; or new rules only, with a line for older cases. Your call.
13. **NOVEL. Source for seed card 1.** The I4C advisory PDF could not be fetched (i4c.mha.gov.in did not answer all day, K9). The only official text found is I4C's own CyberDost Telegram post (t.me, not a government domain). Proposal: keep I4C-ADV-2026-08-01 to 03 as `candidate` from the Telegram post, and switch the source to the PDF when the site is back. Or: the card waits for the PDF.
14. **Contact C12 (Nyaya Setu WhatsApp).** No official page states the number. The same service has an official toll-free number, 14454 (new row C19). Proposal: reject C12 and use C19.
15. **Contact C04 (Money Restoration Portal).** The address `mrm-ncrp.mha.gov.in` is stated only on the portal's own FAQ; MHA releases name the module but not the address. Please confirm it yourself before verifying; fake "money recovery" sites are a known scam.

## Commit rules

- No `Co-Authored-By` line and no other AI credit line.
- Author email is the GitHub no-reply address, set in each clone's local git config. Never a personal email.

## User to-do before given loops

- [x] **Before L03b (CI part) and L04:** first commit and public repo. Done 30 Sep 2026.
- [ ] **Before L03b:** switch on branch protection for `main` in GitHub settings (free now that the repo is public). Claude gives the exact steps in L03b.

- [x] **Before L03a:** install Hugo extended. Installed on the first PC (found, 30 Sep 2026) and on the second PC (0.167.0 extended, 30 Sep 2026).
- [x] **GitHub CLI:** installed on the second PC (2.101.0) and signed in as `satyasairay`, 30 Sep 2026.
- [ ] **For L02 (now):** download the RBI Directions PDF that holds the liability rules for transactions before 1 January 2027. RBI's PDF host shows a human check to scripts, and Claude does not complete those checks. Steps: open https://rbidocs.rbi.org.in/rdocs/notification/PDFs/170MD.PDF in your browser, complete RBI's check if it shows one, and save the file as `C:\Users\USER\Desktop\commonman-playbooks\.cache\sources\src-rbi-04.pdf`. Then tell Claude. Claude extracts paragraphs 64 to 76 and drafts those facts.
- [ ] **For L02 (now):** run the Codex fact check on this PC, where the saved sources are (AGENTS.md, Job 1, mode A). The exact command is in the PR.
- [ ] **Before L05:** find 5 people who have not seen the page (for example a parent, a neighbour, a shopkeeper) for a 10-minute test each.
- [ ] **Before L06:** the VPS steps. Claude writes the exact commands in L06; you run them with admin rights.
- [x] **Before the first Codex fact check (L02):** install Codex CLI. Installed on the first PC (found, 30 Sep 2026; sign-in not checked there). On the second PC: Codex CLI 0.159.2 from npm, signed in with ChatGPT (checked with `codex login status`, 30 Sep 2026).

## Decisions log

| Date | Decision | Why |
|---|---|---|
| 29 Sep 2026 | Non-profit. No income, no donations. | Satya's rule. |
| 29 Sep 2026 | Working name "Commonman Playbooks"; served from satsangee.org for now. | Real name not chosen. "Satsangee" belongs to an established community. |
| 29 Sep 2026 | Hugo static site. No database, no JavaScript. | Loads on 2G, little to attack, nothing to leak. |
| 29 Sep 2026 | Collect nothing from readers. | A store of victim data is a target and brings DPDP duties. Trust. |
| 29 Sep 2026 | Scam pages are six recovery families plus short scam cards. | Most new scams are new lures on old methods. A card reuses verified recovery steps, so a new scam can go live in a day. |
| 29 Sep 2026 | rules/contacts.md is the only source of numbers and links. The build fails on anything else. | Fake helpline numbers are a common scam. One wrong number would undo the site. |
| 29 Sep 2026 | Never list bank phone numbers. Pages say: use the number on the back of your card or in your bank's official app. | Bank numbers change, and fake ones rank high in search. |
| 29 Sep 2026 | AI drafts, Satya merges. Codex checks each claim against the sources. | Two models agreeing is not verification. They share blind spots on Indian details. |
| 29 Sep 2026 | Both engines check claims against the same saved snapshot of each source. | Same evidence for both checkers, and a record of what the page was checked against. |
| 29 Sep 2026 | The layout adds the approved opening line to every playbook and card. | Satya's rule. Panic is the scammer's main tool. |
| 29 Sep 2026 | Odisha first for state notes. | Satya can verify Odisha himself. |
| 29 Sep 2026 | The first scam card ships with F2 in L05: sideloaded adult apps that drain bank accounts (I4C, 26 Aug 2026). | Satya wants new scams in early. |
| 29 Sep 2026 | A scam card links to every family a reader could be in, as branches. | The same scam leaves different readers in different places (money lost or not yet). |
| 29 Sep 2026 | No `Co-Authored-By` line or other AI credit line in commits or PR descriptions. | Satya's ground rule. |
| 29 Sep 2026 | Facts registry (rules/facts.md). Every number, amount, deadline, rule and office name lives there once; pages only reference it. G11 fails bare claims. | Satya checks each fact once. Every format and language shows the same checked words. His review time does not grow with each format. |
| 29 Sep 2026 | Formats (rules/formats.md): web, WhatsApp text, print sheet first; start page after all six families; audio with Odia and Hindi; share images cut until after L17. G12 checks every format. | Satya: "Playbook is one form of presentation only." Information in India moves as WhatsApp forwards and on paper. |
| 29 Sep 2026 | Trust signals (rules/formats.md): evidence one tap away, confidence labels on cards, check dates, scope lines, "what we don't know", public corrections log, commit id in the footer, security.txt, a privacy claim anyone can test. G3 checks they exist. | The site should show an analyst's care without slowing the frightened reader. |
| 29 Sep 2026 | Audio uses a human voice only. No QR codes on sheets for public walls. | Voice cloning and QR sticker swaps are scams the site warns about. |
| 29 Sep 2026 | L03 split into L03a, L03b and L03c. | Too big for one loop after the plan change. |
| 29 Sep 2026 | English pages are pure, simple Indian English. G10 fails the build on Hinglish, on Devanagari or Odia script, and on any word outside the dictionary and rules/allowed-terms.md. | Satya's rule. A reader should meet only plain English words and names they know. |
| 30 Sep 2026 | Opening line (en): "Don't worry. What happened is not in your hands now. What you do next is in your hands." | Satya's words, with the last sentence finished for new English readers and for translation. |
| 30 Sep 2026 | House rules sections 2 to 11 and all allowed terms approved as written. Lakh and crore allowed. | L01. |
| 30 Sep 2026 | Byline: name and date only. The 14 years goes on the Method page. | Repeating it on every page reads as self-promotion. |
| 30 Sep 2026 | AI line: Satya writes it himself. No page goes live until it exists. | It appears on every page, so it must be in his words. |
| 30 Sep 2026 | The repo goes public right after the first commit. | Peers can watch it being built. On the free GitHub plan, branch protection works only on public repos (K5). |
| 30 Sep 2026 | Odia and Hindi opening lines deferred to L14. L01 closes on the English line and the AI line. | Satya: keep Odia and Hindi out for now. They are needed only when Odia and Hindi pages exist, in L14. |
| 30 Sep 2026 | Source ids are `src-<owner>-<NN>` in small letters. Contacts and facts share one Sources table in rules/facts.md. Each source is saved as the original plus a plain-text copy that the checkers read. | One place for every source. The id cannot clash with fact ids or radar ids. Both checkers read the same text. |
| 30 Sep 2026 | A fact statement never contains a phone number, URL or email; the page puts a contact reference beside it. | Keeps G1 simple: every number on a page comes through a contact. |
| 30 Sep 2026 | Facts are drafted only from the text in force. The withdrawn 2017 RBI circular is not used as a source, even though RBI says its text moved "as-is". | Satya's rule: primary source, current text. |

## Adversary rounds

| Date | Loop | Passes | Findings | Fixed |
|---|---|---|---|---|
| (none yet) | | | | |

## Known issues

- K1: The Nyaya Setu WhatsApp number has news sources only, no official source yet. Closes in L02.
- K2: The I4C advisories page has no RSS feed. The radar must compare the HTML listing day to day. Closes in L04.
- K3: Official URL of the I4C Money Restoration Module not found yet. Found on 30 Sep 2026 (contact C04, `mrm-ncrp.mha.gov.in`). Closes when Satya verifies C04.
- K4: satsangee.org has no TLS certificate because Caddy has no site for it. Closes in L06.
- K5: Branch protection on `main` is not switched on yet. It is free now that the repo is public. Until it is on, "only Satya merges" is enforced by engine instructions and by a deploy job that runs only from main. Closes in L03b.
- K6: Four seed cards (digital arrest, task scam, fake investment groups, UPI collect/QR) have only vendor or press sources so far. Each needs an official source before `confirmed`. Closes in L08 and L09.
- K7: The candidate facts in rules/facts.md come from memory and news. None may be used until found in a primary source and verified. Closes for F2 and card 1 in L02; for the rest, in the loop that needs them.
- K8: Contact C18 (the WhatsApp share link) needs WhatsApp's own help page as its source. Found on 30 Sep 2026 (src-whatsapp-01). Closes when Satya verifies C18.
- K9: i4c.mha.gov.in did not answer on 30 Sep 2026, from India (timeouts on ports 80 and 443) or from outside (connection refused). It blocks contact C03, the card 1 advisory PDF, and the radar's main source (S01). Recheck at the start of the next session.
- K10: RBI's PDF host (rbidocs.rbi.org.in) shows a human check to scripts. The liability rules for transactions before 1 January 2027 exist only there (170MD.PDF). Satya downloads the file (user to-do). The radar in L04 will need another way to read RBI (for example the HTML notification pages on www.rbi.org.in, which do load).
- K11: India Code returned HTTP 504 for every BNSS page on 30 Sep 2026. The Zero FIR facts come from the Act as enacted (Gazette), so later amendments are not checked yet.
- K12: The new RBI liability rules (src-rbi-03) cover commercial banks only. Regional rural banks, small finance banks, payments banks and co-operative banks have their own amendments (issued the same day), not saved yet. Many Odisha readers bank with a regional rural bank.
- K13: Evidence quotes are verbatim, so they can hold words G10 forbids on English pages (for example "dalals" in the I4C-MRM-10 quote). L03b must decide whether the evidence layer is exempt from G10, or such quotes must be avoided.
- K14: Source snapshots exist only on the second PC. On another PC, `.cache/sources/` must be fetched again, and rendered or dynamic pages may give a different SHA-256. The fetch script (L03a) should record this.

## Metrics

| Date | Live pages | Verified facts | Verified contacts | Radar runs | Open signals | Median signal to PR | Corrections | Wrong-fact reports |
|---|---|---|---|---|---|---|---|---|
| 29 Sep 2026 | 0 | 0 | 0 | 0 | 0 | n/a | 0 | 0 |
| 30 Sep 2026 | 0 | 0 (62 candidate) | 0 (18 with a source, waiting) | 0 | 0 | n/a | 0 | 0 |
