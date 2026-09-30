# Radar sources

The radar reads these sources. Tier decides what an item can become (PIPELINE.md, "The radar"). The `URL status` column says how far each URL has been checked. L04 verifies every URL the radar uses and records the method that works.

- `read 29 Sep 2026`: the page was fetched and read.
- `seen in search 29 Sep 2026`: a search result showed the URL; the page itself was not read.
- `unverified`: from general knowledge. Must be checked before use.

## Tier: official

| Id | Source | URL | Method | Cadence | URL status |
|---|---|---|---|---|---|
| S01 | I4C advisories | https://i4c.mha.gov.in/advisories.aspx | Compare the listing with the last run; advisories are PDFs; there is no RSS | daily | read 29 Sep 2026 |
| S02 | I4C Cyber Digest | https://i4c.mha.gov.in/cyber-digest.aspx | Compare the listing | weekly | seen in search 29 Sep 2026 |
| S03 | CyberDost (I4C) on X, Facebook, Instagram, YouTube | https://www.youtube.com/c/CyberDostI4C (others to find) | Search, or read by hand | daily | YouTube seen in search 29 Sep 2026; others unverified |
| S04 | PIB press releases (MHA, MeitY, DoT, Finance, Consumer Affairs) | https://pib.gov.in | RSS if it exists, else compare the listing | daily | unverified |
| S05 | PIB Fact Check | X account (handle to confirm) | Search | daily | unverified |
| S06 | RBI press releases | https://www.rbi.org.in | RSS if it exists | daily | unverified |
| S07 | RBI Alert List of unauthorised forex trading platforms | on rbi.org.in (page to find) | Compare the list | weekly | unverified |
| S08 | SEBI press releases and investor alerts | https://www.sebi.gov.in | RSS if it exists | daily | unverified |
| S09 | NPCI press releases and alerts | https://www.npci.org.in | Compare the listing | weekly | unverified |
| S10 | DoT and Sanchar Saathi advisories | https://dot.gov.in and https://sancharsaathi.gov.in | Compare the listing | weekly | unverified |
| S11 | UIDAI press releases | https://uidai.gov.in | Compare the listing | weekly | unverified |
| S12 | CERT-In advisories (only those that affect individuals) | https://www.cert-in.org.in | Compare the listing | weekly | unverified |
| S13 | Odisha Police and the Bhubaneswar-Cuttack Commissionerate Police | X accounts and press notes (to find) | Search | daily | unverified |
| S14 | Telangana Cyber Security Bureau, Hyderabad and Cyberabad police | X accounts (to find) | Search | daily | unverified |
| S15 | Other state police cyber units (Kerala, Maharashtra, Karnataka, Delhi) | X accounts (to find) | Search | weekly | unverified |

## Tier: press

An item from these needs an official source, or two independent press reports, before it becomes a card. Until then it is a `watch` card.

| Id | Source | URL | Method | Cadence | URL status |
|---|---|---|---|---|---|
| P01 | The420.in (Indian cybercrime news) | https://the420.in | RSS if it exists, else search | daily | seen in search 29 Sep 2026 |
| P02 | Odia press: OmmCom News, Sambad, Dharitri | https://ommcomnews.com (others to find) | Search | daily | OmmCom seen in search 29 Sep 2026; others unverified |
| P03 | National press cyber pages: The Hindu, Indian Express, Times of India, Deccan Herald, Tribune | (to find) | Search | daily | unverified |
| P04 | Security vendor reports (for example Quick Heal and Seqrite) | https://www.quickheal.co.in/knowledge-centre/ | Read by hand | quarterly | read 29 Sep 2026 (mid-2026 report) |

## Tier: victim

`watch` only. Never names a company or a person.

| Id | Source | Method | Cadence | URL status |
|---|---|---|---|---|
| V01 | Reddit: r/india, r/LegalAdviceIndia | Search | daily | unverified |
| V02 | X: posts about scams that mention 1930 or cybercrime.gov.in | Search | daily | n/a |
| V03 | Consumer complaint forums | Search | weekly | unverified |

## Tier: forecast

Scams follow new schemes and deadlines. I4C's FASTag Annual Pass advisory came after the pass launched. These sources start a card before the scam wave.

| Id | Source | Method | Cadence |
|---|---|---|---|
| FC01 | New government schemes and registrations (from S04) | Flag any scheme that involves a payment, a registration or a deadline | daily |
| FC02 | Income tax due dates (incometax.gov.in) | Calendar | monthly |
| FC03 | Festival sales: Durga Puja, Diwali, Rath Yatra in Odisha | Calendar, set by hand once a year | yearly |
| FC04 | Exam results: CBSE, CHSE Odisha, BSE Odisha | Calendar | yearly |
| FC05 | New KYC, SIM or banking rule deadlines (from S06, S10, S11) | Flag deadlines that affect individuals | weekly |
