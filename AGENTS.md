# AGENTS.md

Standing brief for any second engine (Codex CLI or another). Read it at the start of every run.

## The project

Commonman Playbooks (working name) publishes one page for each thing that goes wrong in an ordinary Indian life, and short cards for new scams. A person in panic reads these pages on a cheap phone, as a forwarded WhatsApp message, or on a printed sheet. A wrong phone number, a wrong deadline or a wrong step can cost a reader money. Satya (Satyasai Ray) checks and signs everything. Nothing goes live until he merges it.

Every number, amount, deadline, rule and office name lives once, in rules/facts.md. Every phone number, URL and email lives once, in rules/contacts.md. Pages point to them by id.

## Trust rule

The gate is CI, the adversary review, mutation-checked tests, the loop's DONE WHEN and Satya's merge. It is never the author. Your output is evidence for those gates. It is not a decision.

## Job 1: checks (your main job)

Use only the files in the repo and the source snapshots in `.cache/sources/<source id>.*`. They are the exact text the Claude checker used. Fetch nothing from the web. Never use your own memory as a source: "I believe this is true" is `NOT FOUND`. Do not rewrite anything or suggest style changes.

### Mode A: fact check (PR labelled `kind:fact`)

For each new or changed fact block in rules/facts.md, and each new or changed row in rules/contacts.md:
1. Does the quote appear, word for word, in the source snapshot, at the stated location?
2. Does the statement say only what the quote says? Is it broader, narrower, or missing a condition?
3. Does the conditions list carry every condition the source attaches?
4. For kind rule, right or deadline: is the source on a primary domain (rules/facts.md, "Sources")?

Verdict for each fact: `SUPPORTED`, `PARTIAL` (a condition dropped, or the statement goes beyond the quote), `NOT FOUND`, or `CONTRADICTED`. If a snapshot is missing: `NOT CHECKED: snapshot missing`.

Output: one PR comment that starts with `FACT CHECK (codex)`.

| Fact id | Verdict | Quote found at | Statement matches quote? | Conditions complete? | Primary domain? | Note |
|---|---|---|---|---|---|---|

### Mode B: page check (PR labelled `kind:playbook` or `kind:card`)

For each page in the PR, in every format it builds:
1. List every factual claim in the page text: numbers, amounts, deadlines, office names, legal rules, and steps that say something will happen ("the bank must ...", "you will get ...").
2. For each claim: does it come through a fact reference? If it is written as plain text, it is a `BARE CLAIM`, even if it is true.
3. For each fact reference: does the fact fit the place it is used? (For example, a deadline for card fraud used in a step about UPI.)
4. List every phone number, URL and email. Each must be a contact reference to a `verified` contact.

Output: one PR comment that starts with `PAGE CHECK (codex)`.

| # | Claim or reference (as written) | Through a fact reference? | Fits its place? | Note |
|---|---|---|---|---|

| Value | Type | Contact reference to a verified contact? |
|---|---|---|

**How Satya runs it (Codex CLI, on the PC, in the repo folder):**

```
codex exec "Follow AGENTS.md Job 1, mode A, for the facts changed in this branch."
```

```
codex exec "Follow AGENTS.md Job 1, mode B. Page: content/en/playbooks/money-left-my-account.md"
```

Both modes only read files. They need no write access and no network.

## Job 2: engineering loops

You work only from a LOOP CARD that Satya or the main Claude session gives you. No card, no work.

```
LOOP CARD
LOOP id:
GOAL: (one line)
FILES in bounds:
FILES out of bounds:
DONE WHEN: (measurable)
TESTS FIRST: (the failing tests to write before the fix)
FORBIDDEN: (anything extra for this card)
HANDOFF evidence: (what the PR must show)
```

- Branch: `loop/<id>-cx`. Open a PR. Never merge.
- PR description: the filled card, the pasted test and gate output, and screenshots for anything visible.
- Every test that guards a control must be mutation-checked: break the control, show red, restore from a backup copy, show green.

## Never

- merge, deploy, or push to `main`
- add `Co-Authored-By` or any other AI credit line to a commit or PR description
- edit CLAUDE.md, STATE.md, LOOP.md, AGENTS.md, rules/contacts.md, rules/facts.md or rules/allowed-terms.md
- touch secrets, SSH keys, GitHub settings or the VPS
- write a phone number, URL, email, number, amount, deadline or rule into page text instead of a reference
- add JavaScript, trackers, forms, cookies, web fonts or CDNs to the site
- set `draft: false`, `verified_by` or `verified_on` on any page, or `verified` on any fact or contact. Only Satya sets these.
