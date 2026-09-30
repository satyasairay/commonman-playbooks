# Taxonomy

Most new scams are new lures on a few old methods. The families below describe what happened to the reader, not what the scam is called. Each family has one deep recovery playbook. Scam cards are short and point to the families.

## The six families

| Id | Playbook title (reader's words) | Slug | What happened | First-hour priority |
|---|---|---|---|---|
| F1 | I sent money because I was tricked | tricked-into-paying | The reader made the payment after a lie: fake investment, part-time task, fake seller, fake refund, fake government fee, an approved UPI collect request. | Report fast so the money can be frozen. Keep the payment reference and the chats. |
| F2 | Money left my account and I didn't send it | money-left-my-account | Someone else moved the money: stolen OTP or PIN, malware, screen-sharing app, SIM swap, cloned fingerprint (AEPS). | Report fast. Block cards, UPI and net banking. Tell the bank in writing. |
| F3 | My phone or WhatsApp was taken over | phone-or-whatsapp-taken-over | Someone controls the reader's phone or account: sideloaded app or profile, accessibility abuse, stolen WhatsApp code, stolen phone. | Cut the attacker off. From another phone, block the SIM and payments. Recover WhatsApp. Warn contacts. |
| F4 | Someone is using my identity | someone-using-my-identity | The reader's identity was used to open accounts, take loans, get SIMs or pass KYC: deepfake, injected video, cloned fingerprints, leaked documents. | Lock Aadhaar biometrics. Check Aadhaar authentication history, credit reports and SIMs in the reader's name. |
| F5 | I am being threatened right now | threatened-right-now | Fear, fake authority and isolation: "digital arrest", sextortion, fake police, customs or courier, loan-app harassment. | End the call. No real agency arrests anyone on a video call. Do not pay. Tell someone you trust. Report. |
| F6 | I clicked, shared or installed something, but no money is lost yet | clicked-shared-installed | The early stage of F2, F3 or F4. | Disconnect. Remove the app or profile. Change passwords from another device. Alert the bank. Watch the account. |

Each first-hour priority above is a summary for mapping. The playbook states the real steps, each with its source.

## Mapping rules

- A card links to every family a reader of that scam could be in, as branches. Example: "If money left your account: F2. If you have not lost money yet: F6."
- The first family in the card's `families` list is its primary family, which sets its label.
- If a scam fits no family, do not force it. Open an issue labelled `family:none`. A seventh family needs Satya's approval.

## Seed scam cards

Twelve cards to start. The first eight come from the I4C advisories page (listing read on 29 Sep 2026). Status stays `watch` until an official source for the card is snapshotted and checked.

| # | Card | First seen (source date) | Source | Tier | Families | Ships in |
|---|---|---|---|---|---|---|
| 1 | Sideloaded adult apps that drain bank accounts | 26 Aug 2026 | I4C advisory | official | F2, F6 | L05 |
| 2 | Fake regulator or executive messages that lead to WhatsApp takeover through Windows files | 22 Jun 2026 | I4C advisory | official | F3, F1 | L10 |
| 3 | AI-driven bypass of identity checks at financial firms | 10 Jun 2026 | I4C advisory | official | F4 | L11 |
| 4 | iPhone theft followed by account takeover | 5 May 2026 | I4C advisory | official | F3, F2 | L10 |
| 5 | Crypto scams aimed at Trust Wallet users | 20 Apr 2026 | I4C advisory | official | F2, F1 | L08 |
| 6 | Android "God Mode" malware that will not uninstall | 16 Mar 2026 | I4C advisory | official | F3, F2 | L10 |
| 7 | Fake FASTag Annual Pass offers | 11 Feb 2026 | I4C advisory | official | F1, F6 | L08 |
| 8 | Sideloaded iOS apps through configuration profiles | 15 Jan 2026 | I4C advisory | official | F3, F6 | L10 |
| 9 | "Digital arrest" video calls | long-running | I4C public advisory (reported in press; PDF to find) | official, source to snapshot | F5, F1 | L09 |
| 10 | Part-time task scams | long-running | Quick Heal mid-2026 report (vendor) | press; official source needed | F1 | L08 |
| 11 | Fake investment groups on WhatsApp and Telegram | long-running | Quick Heal mid-2026 report (vendor) | press; official source needed | F1 | L08 |
| 12 | UPI collect requests and QR codes | long-running | Quick Heal mid-2026 report (vendor) | press; official source needed | F1 | L08 |

I4C also listed two ransomware advisories in 2026 (cPanel and WHM, 15 Jun; NAS devices at CA firms, 2 Mar). They target businesses, not individuals, so they are out of scope.

## Life events (after L17)

| Id | Playbook title (reader's words) |
|---|---|
| E1 | My phone is lost or stolen |
| E2 | Someone in my family died, and I have to deal with the paperwork |
| E3 | I lost my documents (Aadhaar, PAN, passport, driving licence, mark sheet) |
| E4 | I was in a road accident |
| E5 | The hospital or insurance company rejected my claim |
| E6 | An online order or a service cheated me |
| E7 | The police will not register my complaint |
| E8 | My land record is wrong (Bhulekh, Odisha) |

E1 overlaps with F3. Its first steps belong in F3, and E1 adds the rest (device block, replacement SIM, insurance).
