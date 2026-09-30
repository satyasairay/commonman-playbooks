# Facts registry

Every number, amount, deadline, rule, right and office name that a page states comes from this file. A page never types these itself. It points to a fact by its id, and the build puts in the checked words, with the evidence one tap away. Satya checks each fact once. Every page, every format and every language that uses it then shows the same checked words.

Changes to this file are NOVEL: Satya approves each one.

## How pages use facts and contacts

- **Fact reference:** the `fact` shortcode with the fact id (for example `RBI-LIAB-01`). It shows the fact's statement in the page's language and adds an evidence marker. One tap opens the source, the exact quote, the date checked and the fact id.
- **Contact reference:** the `contact` shortcode with the contact id from rules/contacts.md (for example `C01`).
- **G11** fails the build if page text outside these references contains a number, an amount, a time period, a percentage, a section number, or the name of an Act, a rule or a circular. Step numbers are exempt.
- Built in L03a (the references) and L03b (G11).

## Fact ids

- Form: `<OWNER>-<TOPIC>-<NN>`, for example `RBI-LIAB-01`. Capital letters, no spaces.
- An id is never reused. If a fact changes, the new wording becomes a new version. The old version stays here marked `superseded`, and the corrections log records the change.

## Sources

Facts point to sources by id. Each source is saved once to `.cache/sources/<source id>`, with its SHA-256.

For rules, rights and deadlines, only primary sources count: the statute (indiacode.nic.in), the gazette (egazette.gov.in), or the regulator's own circular or page (for example rbi.org.in, sebi.gov.in, uidai.gov.in, dot.gov.in, i4c.mha.gov.in). G9 checks the domain.

| Source id | Title | Owner | URL | SHA-256 | Fetched |
|---|---|---|---|---|---|
| (none yet) | | | | | |

## Entry format

One block per fact. The block below shows the format only. It is not a real fact.

### EXAMPLE-FORMAT-01

- **kind:** deadline, rule, right, amount, office, process, or advisory
- **statement.en:** the exact words pages show, in pure, simple Indian English
- **statement.or / statement.hi:** added in L14, each signed by a human reader of that language
- **conditions:** every condition the source attaches. These carry the law. Never drop one.
- **applies to:** all, or a state code such as OD
- **source:** source id, plus the section, paragraph or page number
- **quote:** the exact words in the source, 40 words at most
- **verified on / by:**
- **recheck by:** 180 days after verification for laws; 90 days for anything a regulator changes often
- **status:** candidate, verified, superseded, or rejected
- **version:** v1

## Facts

None verified yet.

## Candidate facts to find (work queue for L02 and later loops)

These are topics that the first playbooks need. They come from memory and from news read on 29 Sep 2026. None may be used until it is found in a primary source and verified. The words on a page will come from the source, not from this list.

| Topic | Needed by | Where to look |
|---|---|---|
| Customer liability for unauthorised electronic banking transactions: the reporting windows and what the customer pays in each | F2 | RBI circular on limiting customer liability (2017), rbi.org.in |
| How soon the bank must credit the amount back while it investigates, and the deadline to settle the complaint | F2 | the same RBI circular |
| When a customer can go to the RBI Ombudsman | F1, F2 | RBI Integrated Ombudsman Scheme 2021, rbi.org.in |
| Report to 1930 and cybercrime.gov.in quickly so money can be frozen | F1, F2 | I4C or Home Ministry page, cybercrime.gov.in |
| The I4C Money Restoration Module: who can apply, and how | F1, F2 | I4C page (not found yet, known issue K3) |
| Credit bureaus must alert you when your credit report is accessed | F4 | RBI circular to credit information companies (2023) |
| Compensation when a credit complaint is not settled in time | F4 | the same RBI framework |
| SMS is blocked for a period after a SIM replacement | F3, F4 | DoT order |
| How far back you can see your Aadhaar authentication history | F4 | uidai.gov.in |
| What the Aadhaar biometric lock blocks, and how to unlock it for a short time | F4 | uidai.gov.in |
| A police station must register an FIR even if the crime happened elsewhere (Zero FIR) | F1 to F5, E7 | BNSS 2023, section 173, indiacode.nic.in |
| No police officer or agency arrests anyone on a video call | F5 | I4C advisory on "digital arrest" |
| What the sideloaded adult apps do, per the advisory | seed card 1 | I4C advisory, 26 Aug 2026 |
