# House rules

Every draft follows these rules. The drafter reads this file before writing anything, and the adversary checks against it. Satya approves each section in L01. Section 13 grows each time he rejects a draft for a reason that could happen again.

| Section | Status | Date | Initials |
|---|---|---|---|
| 1 Opening line | en approved; or and hi deferred to L14 | 30 Sep 2026 | SR |
| 2 The reader | approved | 30 Sep 2026 | SR |
| 3 Voice and language | approved | 30 Sep 2026 | SR |
| 4 Page structure | approved | 30 Sep 2026 | SR |
| 5 Numbers, links and names | approved | 30 Sep 2026 | SR |
| 6 Deadlines and legal claims | approved | 30 Sep 2026 | SR |
| 7 Never | approved | 30 Sep 2026 | SR |
| 8 Always | approved | 30 Sep 2026 | SR |
| 9 Plain words | approved | 30 Sep 2026 | SR |
| 10 Prose checks | approved | 30 Sep 2026 | SR |
| 11 Languages | approved | 30 Sep 2026 | SR |
| 12 Signature and AI line | signature approved; AI line open (Satya writes) | 30 Sep 2026 | SR |
| 13 Rejections | open log | | |

## 1. Opening line

Every playbook and scam card opens with this line. The layout adds it from the i18n files, so a draft never writes it and cannot leave it out.

| Language | Line | Status | Date | Initials |
|---|---|---|---|---|
| en | Don't worry. What happened is not in your hands now. What you do next is in your hands. | approved | 30 Sep 2026 | SR |
| or | (Satya writes, in L14) | deferred to L14 | 30 Sep 2026 | SR |
| hi | (Satya writes, in L14) | deferred to L14 | 30 Sep 2026 | SR |

The line stays one short line, so pages where time matters (money just left, someone is threatening you right now) reach the clock at once. It is never machine-translated.

## 2. The reader

Write for this person:
- Something just went wrong and they are frightened. The scammer may still be on another call.
- They are on a cheap Android phone, maybe on a slow connection.
- They may be using a smartphone for the first time, or they may be old.
- They may read Odia or Hindi better than English.
- They have never heard of RBI circulars or IT Act sections, and they should not need to.

If a step would confuse this person, the step is wrong, however correct it is.

## 3. Voice and language

English pages are in pure, simple Indian English.

- **Pure.** No Hindi, Odia or other Indian-language words written in English letters (for example "karein", "paisa", "jaldi", "ji"), even when a source uses them. No Devanagari or Odia script on an English page. The only exceptions are the names and terms in rules/allowed-terms.md, such as Aadhaar or Sanchar Saathi, used as names. G10 fails the build on anything else.
- **Simple.** Common words and short sentences. Aim for 15 words or fewer in a sentence. G10 flags any sentence over 25 words.
- **Indian.** ₹ for money, dates as 29 September 2026, British spelling (organise, licence, centre). Lakh and crore are allowed (₹1.5 lakh). Digits use Indian grouping (₹1,50,000).
- No American idiom or slang ("ballpark", "touch base", "heads-up").
- No old office English: "kindly", "do the needful", "revert" for reply, "intimate" for tell, "the same" for it. See section 9.
- Talk to the reader as "you". Say what to do: "Call 1930", not "Victims are advised to contact the helpline".
- Steps are short. One action per step. Start each step with a verb.
- Name things the way the reader sees them. If an official screen uses a term, use that term once and explain it in plain words.
- Calm and direct. No exclamation marks.
- Say it once. No summary at the end of a page.

## 4. Page structure

The order never changes. The layout adds the parts marked (layout).

This is the web format. The WhatsApp text and the print sheet are built from the same page and stop after the first steps (rules/formats.md).

**Playbook:**
1. Opening line (layout)
2. Scope (layout, from front matter): what this page covers, and what it does not
3. The clock (layout, from the fact ids in front matter): the deadlines that decide the outcome, most urgent first
4. Do this now: 5 steps at most. The first steps must stand alone, because the WhatsApp text and the print sheet stop there.
5. Keep these: the evidence to save
6. Where to go, in order: for each place, what to say and what you get back
7. If they don't act: how long to wait, and where to go next
8. Don't
9. Your rights: at most two lines each
10. What we don't know yet (only if something is unsettled)
11. Letters: fill-in templates
12. State notes (Odisha first)
13. Evidence layer, verified-by line, check dates and no-contact line (layout)

**Scam card:**
1. Opening line and confidence label (layout)
2. What it looks like
3. Red flags
4. If this happened to you: one link per family branch, for example "If money left your account" and "If you have not lost money yet"
5. Who has warned about it (layout, from the advisory facts)
6. Evidence layer, verified-by line, check dates and no-contact line (layout)

## 5. Numbers, links and names

- Every phone number, WhatsApp number, URL and email goes in through a contact reference to a `verified` row in rules/contacts.md. G1 fails the build on anything else.
- Write numbers in full. Never use shortened links.
- Never list a bank's phone number. Write: "Call the number on the back of your debit card, or the one in your bank's official app."
- Never name a private company as a scammer unless an official source names it. Never name a private person.
- Never link to a page that sells a service.

## 6. Deadlines and legal claims

- Every number, amount, deadline, rule, right and office name goes in through a fact reference to a `verified` fact in rules/facts.md. A page never types them. G11 fails the build on anything else.
- Each deadline fact says four things: what to do, within how long, counted from when, and under which rule.
- Sources for rules and deadlines are primary: the statute, the gazette, the regulator's circular, or the official portal page. Never a news story or a law-firm blog.
- Keep the conditions. If a rule says "within 3 working days, when the fraud was not your fault", the page says both parts. Hedges like these carry the law. They are not filler.
- If something is not known or not settled, say so plainly.

## 7. Never

- Promise an outcome. Not "you will get your money back". Say what the rule says and what usually happens next, if a source says it.
- Ask the reader for anything: not details, not money, not a message.
- Point to paid services, named lawyers or "recovery agents".
- Blame the reader. No "you should have".
- Use fear to push action. Deadlines are stated as facts.
- Use a term the reader would not know without explaining it once.
- Copy text from another site.

## 8. Always

- Say what the reader gets back at each step: a complaint number, a reference number, a written reply.
- Say what to do when the people responsible do not act.
- Say what is not known.
- Keep evidence steps before cleanup steps. A phone wiped too early loses the proof.

## 9. Plain words

| Write | Not |
|---|---|
| money | funds |
| bank | financial institution |
| call | contact, reach out to |
| phone | device, handset |
| give | furnish, provide |
| tell | inform, intimate |
| before | prior to |
| about | regarding, with respect to |
| use | utilise |
| help | assist, facilitate |
| start | commence, initiate |
| people | individuals |
| do | implement |
| please | kindly |
| reply | revert |
| it | the same |

## 10. Prose checks

These apply to prose: the Method page, "What it looks like" on cards, and any paragraph longer than two sentences. They do not apply to step lists, where short and uniform is right.

- Em-dashes: none on pages under 300 words, and at most one per 1,000 words.
- No arrow characters.
- No "not just X, but Y", no "it's not X, it's Y", no lists of three where the content does not come in threes.
- No opening lines like "In today's digital age".
- None of these words: delve, crucial, robust, seamless, navigate (as a metaphor), leverage, landscape, empower, journey, unlock, vital, comprehensive, game-changer, testament.
- Vary sentence length in prose. Read one paragraph aloud. If it sounds like a metronome, rewrite it.
- End on the last real point. No closing summary.

## 11. Languages

- English first. Odia and Hindi follow in L14.
- A machine may draft a translation. It never goes live until a human who reads that language signs it (`verified_by` on that language's page).
- Satya writes or approves the opening line in each language (section 1).
- Odia and Hindi pages use plain, everyday language, the way people speak it. Common borrowed words such as bank, mobile and OTP are fine. Heavy official or Sanskrit-based words are not. The human reviewer for each language decides.

## 12. Signature and AI line

- Verified-by line, on every page: "Verified by Satyasai Ray on 30 September 2026." Name and date only. Always day, month in words, year. The 14 years in security operations appears once, on the Method page.
- AI line, on the Method page and in the site footer: Satya writes it in his own words (open). Until then, no page goes live.

## 13. Rejections

When Satya rejects a draft for a reason that could happen again, the main session adds a row here and, if needed, a rule to the section it belongs to.

| Date | Page | Reason (Satya's words) | Rule added |
|---|---|---|---|
