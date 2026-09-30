# Formats

A playbook page is one way to show the facts. Every format below is built from the same checked facts and contacts. A fact checked once is correct in every format and every language. Satya checks each fact for truth once. For each format he only checks how it looks and reads.

## The formats

| Id | Format | For whom | Built from | Limit | First in |
|---|---|---|---|---|---|
| WEB | Web page: playbook or scam card | anyone with the link | page file, facts, contacts | under 50 KB, no JavaScript | L05 |
| WA | WhatsApp text | people who get their news as forwards | title, opening line, the first steps, 1930, page link | 700 characters, one phone screen | L05 |
| PRINT | One-page A4 sheet, black and white | bank branches, panchayat offices, police station notice boards, a family's fridge; readers without a phone | page, facts, contacts | exactly one page; text 12 pt or larger | L05 |
| START | "What happened?" start page | a frightened person who does not know which problem they have | the families and their first questions | 3 questions deep at most; no JavaScript | L12b |
| AUDIO | Audio, 60 to 90 seconds, in Odia and Hindi first | people who do not read easily | a script built from the page, read by a human | 32 kbps mono MP3, under 400 KB; transcript on the page | L14 |
| IMAGE | Share image for Facebook, Instagram and X | people who scroll, not search | title and first steps | not planned yet | after L17 (kill list) |

## Rules for every format

- Same facts, same order, same words. A format may stop early (the WhatsApp text stops after the first steps). It never changes a step or adds one.
- Every format carries the opening line, the page link, the no-contact line and the verified-on date.
- Every format passes G1, G6, G8, G10 and G11, and its own limit (G12).

## Notes on each format

**WEB.** Two layers. On top, the reader layer: calm and simple, steps first. One tap underneath, the evidence layer: sources, quotes, fact ids and dates. The layer uses the HTML `<details>` element, so it needs no JavaScript.

**WA.** Plain text, with WhatsApp's own bold (text between asterisks) and nothing else. No shortened links, no capital-letter urgency, no "forward to 10 people". It must not look like the scam forwards the site warns about. The page offers a share link on `https://wa.me/?text=`, which opens WhatsApp with the text filled in. The site learns nothing when someone taps it. (Contact C18, pending.)

**PRINT.** A print page on the site, plus a PDF built in CI with WeasyPrint (no browser needed). The full web address is printed in large letters. Sheets meant for public walls carry **no QR code**: a sticker over the code can send people to a fake page, which is exactly how the QR scams in seed card 12 work. Handouts may carry a QR code, always with the address printed beside it and the line "Check that the address shows satsangee.org before you trust the page."

**START.** The first question is always "Is someone threatening you, or asking you for money, right now?" A yes goes straight to F5. The most urgent case is handled first, as in triage.

**AUDIO.** A human voice: Satya's or a named volunteer's. Never an AI voice. Voice cloning is one of the scams the site warns about, so an AI voice would teach readers the wrong habit. The transcript sits under the player.

## Trust signals

The reader layer stays simple. These signals live in the evidence layer and in the site's frame, where a peer will look and a frightened reader will not be slowed down.

| Signal | Where it shows | Checked by |
|---|---|---|
| Every fact has an evidence marker: source, exact quote, date checked, fact id | inline, one tap | G2, layout |
| Scam cards carry a confidence label: "Confirmed by (agency) on (date)" or "Watch: reported, not yet confirmed". The two are never mixed. | top of each card | G2 |
| "Checked on" and "next check by" dates on every page. A page past its check date says so plainly. | page footer | G3 |
| Scope: "This page covers ... It does not cover ..." | under the title | adversary, Satya |
| "What we don't know yet", when something is not settled | its own short section | adversary, Satya |
| Corrections log: every mistake, dated, with how long it was live and what changed. No silent edits. | /corrections/ | G3 |
| The commit id and build date, linking to the change history once the repo is public | site footer | G3 |
| security.txt, and a "Report a mistake" link | /.well-known/security.txt, footer | G3 |
| A privacy claim anyone can test: "This site sets no cookies and loads nothing from other sites. You can check this in your browser." | footer | G4, outside curl |
| The Method page: families, source tiers, gates, what AI does and does not do | /method/ | L07 |

## What the design leaves out

Stock photos, emojis, "AI-powered" labels, red alarm banners, countdown timers, pop-ups, carousels and web fonts. The site uses system fonts, black text on white, one accent colour for the clock, and large tap targets. It reads well at 320 pixels wide and prints cleanly.
