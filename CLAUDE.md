# Commonman Playbooks: Claude entry point

"Commonman Playbooks" is a working name. The real name is not chosen yet (STATE.md, inbox item 1). The site is served from satsangee.org for now.

**User:** Satya (Satyasai Ray). 14 years in security operations: SOC, detection engineering, DLP, playbooks and SOPs. Lives in Odisha. This is a non-profit project with no income.
**Product:** One page for each thing that goes wrong in an ordinary Indian life, plus a radar that finds new scams early. Each page says what to do now, in what order, by when, and what to do when the people responsible do not act.
**Output style:** Spine files use ASD-STE100 simple English. Public text follows rules/house-rules.md.

## Boot order
1. STATE.md: where we are, the next loop, the user inbox.
2. LOOP.md: the protocol, the loops, the hard gates.
3. PIPELINE.md and RUNBOOK.md when the loop touches them. rules/ when the loop touches content.

## /next
Run the loop that STATE.md names as next. Follow THE PROTOCOL in LOOP.md. Stop only at the loop's DONE WHEN or at a user-only gate.

## Rules that never bend
- Nothing is published unless Satya merges it. Engines open pull requests only.
- Every phone number, URL and email on the site comes from rules/contacts.md, and every number, amount, deadline, rule and office name from rules/facts.md, only through references to `verified` rows. Facts are checked once; every format (rules/formats.md) is built from them.
- The site collects nothing: no forms, accounts, cookies, analytics, third-party requests or access logs.
- Every playbook and scam card opens with the approved opening line. The layout adds it.
- The VPS is read-only for Claude. Every server change is a USER DOES step.
- Legal and regulatory facts come from the primary source (statute, gazette, regulator page), never from memory.
- No `Co-Authored-By` line or any other AI credit line in commits or PR descriptions. Satya's ground rule. Never suggest breaking it.
- English pages are pure, simple Indian English. No Hinglish. See rules/house-rules.md, section 3, and gate G10.
- Single writer: only the main Claude session edits STATE.md and LOOP.md.
- This is a Windows PC. Follow the shell rules in Satya's global CLAUDE.md, and pass them to every subagent.
