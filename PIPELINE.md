# PIPELINE.md

How a signal becomes checked facts, and how checked facts become live pages in every format. Each stage names who does it, what starts it, and what it leaves behind. Parts that do not exist yet say which loop builds them.

## Two kinds of change

- **Fact PR** (`kind:fact`): adds or changes rows in rules/facts.md or rules/contacts.md. Checked for truth against the source.
- **Page PR** (`kind:playbook` or `kind:card`): adds or changes a page. It may only use facts and contacts that are already `verified`. Checked for bare claims, reading and format.

A page that needs a new fact waits for the fact PR to merge. On a busy day both can be reviewed together, but the fact PR merges first.

## Stages

| # | Stage | Who | Starts when | Leaves behind | Built in |
|---|---|---|---|---|---|
| 0 | Signal | radar agent | daily at 07:00 IST | a GitHub issue from the `scam-signal` template, with labels | L04 |
| 1 | Triage | main Claude session | a new signal issue | labels `family:` and `status:`, a one-line reason, and a list of the facts the card would need | L04 |
| 2 | Snapshot | `scripts/sources/fetch` | a new source is added to the facts sources table | the source saved in `.cache/sources/<source id>`, with SHA-256 and fetch date | L03a |
| 3a | Draft facts | drafter agent | triage lists facts that are not yet verified | branch `draft/fact-<topic>`, a fact PR with `candidate` rows | L02 |
| 3b | Draft page | drafter agent | every fact it needs is verified | branch `draft/<kind>-<slug>`, a page PR | L05 |
| 4 | Machine gates | CI, no AI | PR opened or updated | pass or fail for G1 to G4, G6 to G12 | L03b, L03c |
| 5 | Claude checks | source-checker (mode A for facts, mode B for pages) and adversary | gates green | PR comments `FACT CHECK (claude)` or `PAGE CHECK (claude)`, and `ADVERSARY` | L02, L05 |
| 6 | Cross-engine check | Codex CLI on Satya's PC | Claude checks done | PR comment `FACT CHECK (codex)` or `PAGE CHECK (codex)` | L02, L05 |
| 7 | Human gate | Satya | stages 4 to 6 done | merge, or reject with a reason | always |
| 8 | Publish | CI | merge to `main` | every format built (web, WhatsApp text, print PDF), gates run again, rsync to the VPS, outside check with curl | L06 |
| 9 | Watch | scheduled jobs | weekly or monthly | issues for source drift (naming every fact and page affected), facts past their recheck date, and impersonation | L15, L16 |

A rejection at stage 7 goes back to stage 3a or 3b. If the reason is a pattern, the main session adds it to rules/house-rules.md, section 13, so the drafter does not repeat it.

## Service levels

- Official advisory to draft card PR: 24 hours, including its fact PR (from L13).
- Press or victim signal to watch-card PR: 48 hours (from L13).
- Satya's review: no target. He sets the pace.
- Wrong-fact report that could cost a reader money or safety: page pulled within 1 hour of Satya seeing it (RUNBOOK R1), fix within 24 hours, entry in the corrections log.
- A fact past its recheck date opens an issue. 30 days after that date, G2 fails every page that uses it. An emergency deploy (commit message starting `emergency:`, RUNBOOK R1) may skip G2 once, and the skip is logged in STATE.md.

## Tools

| Tool | Role | Account | Runs on |
|---|---|---|---|
| Claude Code | main engine: triage, drafting, checks, site code | Max 20x | Satya's PC; the daily radar as a cloud routine or a local scheduled task (chosen in L04) |
| Codex CLI | second engine: fact and page checks (AGENTS.md, Job 1) | ChatGPT Pro, signed in with ChatGPT | Satya's PC only. Running it in CI would need a paid API key. |
| GitHub | repo, issues, PRs, Actions | satyasairay | cloud |
| Hugo (extended) | builds the site and the WhatsApp text | free | PC and Actions |
| WeasyPrint | builds the one-page print PDF | free | Actions |
| Python 3 | fact export, gate scripts, source snapshots, radar parsers | free | PC and Actions |
| Caddy | web server with automatic HTTPS | already installed | VPS |

## Repo layout (target, after L03c)

```
content/
  en/  playbooks/<slug>.md   scams/<slug>.md   method.md   corrections.md
  or/  (same slugs, Odia)
  hi/  (same slugs, Hindi)
archetypes/       playbook.md  scam-card.md
i18n/             en, or, hi: opening line, no-contact line, labels
layouts/          web page, WhatsApp text, print sheet, shortcodes fact and contact
static/.well-known/security.txt
rules/            house rules, taxonomy, sources, contacts, facts, formats, allowed terms (not published)
scripts/facts/    export facts and contacts to Hugo data files (verified rows only)
scripts/gates/    G1 to G4, G6 to G12
scripts/sources/  fetch and fingerprint sources
scripts/radar/    source parsers
.claude/agents/   radar, drafter, source-checker, adversary
.github/          PR template, issue templates, workflows
.cache/           source snapshots (not committed)
```

## Labels

- `kind:fact`, `kind:playbook`, `kind:card`, `kind:event`, `kind:engineering`
- `family:F1` to `family:F6`, `family:none`
- `tier:official`, `tier:press`, `tier:victim`, `tier:forecast`
- `status:new`, `status:watch`, `status:confirmed`, `status:dup`, `status:ignore`
- `format:web`, `format:whatsapp`, `format:print`, `format:audio`
- `harm:high` for wrong-fact reports that could cost a reader money or safety

## Branches

- `main`: what is live. Only Satya merges into it. The deploy job runs only from `main`.
- `draft/fact-<topic>`: fact drafts.
- `draft/<kind>-<slug>`: page drafts.
- `loop/<id>`: engineering loops by Claude.
- `loop/<id>-cx`: engineering loops by Codex.

Commits and PR descriptions carry no `Co-Authored-By` line and no other AI credit line.

Known issue K5: branch protection on `main` is not switched on yet (free, since the repo is public). Until it is on, "only Satya merges" is enforced by engine instructions and by the deploy job running only from `main`. Closes in L03b.

## Deploy (built in L06)

- A VPS user `cmp-deploy` whose SSH key is limited by rrsync to `/var/www/satsangee/site`. That key can write nothing else on the server.
- On merge to `main`: Actions exports the verified facts, builds with Hugo, builds the print PDFs, runs the gates again, then rsyncs `public/` with `--delete`.
- After the rsync, Actions checks from outside: HTTPS works, the security headers are present, there is no `Set-Cookie`, security.txt is served, and the changed pages return 200.
- Caddy serves static files only. It writes no access log for this site.
- Secrets live only in GitHub Actions: `DEPLOY_SSH_KEY` and `DEPLOY_KNOWN_HOSTS` (a pinned host key).

## The radar (built in L04 and L13)

- Sources and tiers: rules/sources.md.
- Tier `official`: an item can become a `confirmed` card, through an advisory fact.
- Tier `press`: needs an official source, or two independent press reports, before a card. Until then, `watch`.
- Tier `victim`: `watch` only, and never names a company or a person.
- Tier `forecast`: a new government scheme, deadline, festival sale or exam result, where scammers usually follow. It can start a card before the scam wave.
- The radar only files issues. It never drafts and never publishes.
- Dedupe: before filing, the radar searches open and closed issues and existing cards for the same scam.
