# RUNBOOK.md

What to do when something goes wrong with the site itself. Each entry says from which loop it works and when it was last drilled. An entry that has never been drilled is not trusted yet.

## R1 · Pull a wrong page (target: under 10 minutes)

Works after: L06. Last drilled: never.

Use when a live page has a wrong phone number, a wrong deadline, a step that could cost someone money, or anything a scammer could use.

1. On the PC, in the repo: `git revert <commit that added or changed the page>`. If you are not sure which commit, set `draft: true` in the page's front matter and commit that.
2. Push to `main` with the commit message starting `emergency:`. The deploy job runs.
3. If Actions is down: log in to the VPS with admin rights and delete the page's folder under `/var/www/satsangee/site/<lang>/<section>/<slug>/`.
4. Check from outside: `curl -sI https://satsangee.org/<lang>/<section>/<slug>/` returns 404.
5. Open or update the issue with label `harm:high`. Record the time taken in STATE.md, under Known issues and Adversary rounds.
6. If a fact was wrong, mark it `superseded` or `rejected` in rules/facts.md. Every page and format that used it rebuilds without it.
7. Add an entry to the corrections page: the date, what was wrong, how long it was live, and what changed. Never fix a live mistake silently.

## R2 · Deploy by hand

Works after: L06. Last drilled: never.

Use when Actions is down and a fix must go out.

1. Build on the PC: `hugo --minify`
2. Run the gates on the PC (L03b names the command).
3. `rsync -rlt --delete public/ cmp-deploy@satsangee.org:/`. rrsync maps `/` to the site folder.
4. Check from outside, as in R1 step 4.

## R3 · Roll back the whole site

Works after: L06. Last drilled: never.

1. In GitHub Actions, run the deploy workflow by hand with the last good commit as the ref.
2. Check from outside.
3. Record in STATE.md.

## R4 · A wrong-fact report arrives

Works after: L05.

1. Read it within 24 hours.
2. Could a reader lose money, time or safety by following the page? If yes, label `harm:high` and do R1 first. Fix after.
3. If no: fix through the normal pipeline. If a fact was wrong, fix it in a fact PR first, and add a corrections entry.
4. Thank the reporter in the issue. Remove any personal data they posted.

## R5 · The radar is silent for 48 hours

Works after: L04.

1. Check the routine or scheduled task log.
2. Check whether a source page changed its layout (the parser returns zero items).
3. Run the radar by hand once. Record the cause in STATE.md.

## R6 · Someone pretends to be the project or Satya

Works after: L16. Last drilled: never.

1. Take screenshots with the date and the URL or number visible.
2. Report it to the platform (WhatsApp, Telegram, X, Instagram, Facebook).
3. If they asked anyone for money, report it at cybercrime.gov.in or on 1930.
4. Add a warning to the site (NOVEL: Satya approves the text).

## R7 · A source page changed

Works after: L15.

1. Open the drift issue. It lists every fact built on the source, and every page and format that uses those facts.
2. Re-check each fact against the new snapshot.
3. If the fact still holds, verify it again (new date). If not, write a new version in a fact PR and mark the old one `superseded`. Every page and format that uses it rebuilds.
4. If a live page showed the old wording, add a corrections entry.
