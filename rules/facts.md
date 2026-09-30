# Facts registry

Every number, amount, deadline, rule, right and office name that a page states comes from this file. A page never types these itself. It points to a fact by its id, and the build puts in the checked words, with the evidence one tap away. Satya checks each fact once. Every page, every format and every language that uses it then shows the same checked words.

Changes to this file are NOVEL: Satya approves each one.

## How pages use facts and contacts

- **Fact reference:** the `fact` shortcode with the fact id (for example `RBI-LIAB-01`). It shows the fact's statement in the page's language and adds an evidence marker. One tap opens the source, the exact quote, the date checked and the fact id.
- **Contact reference:** the `contact` shortcode with the contact id from rules/contacts.md (for example `C01`).
- **G11** fails the build if page text outside these references contains a number, an amount, a time period, a percentage, a section number, or the name of an Act, a rule or a circular. Step numbers are exempt.
- A fact statement never contains a phone number, URL or email. The page puts a contact reference next to it.
- Built in L03a (the references) and L03b (G11).

## Fact ids

- Form: `<OWNER>-<TOPIC>-<NN>`, for example `RBI-LIAB-01`. Capital letters, no spaces.
- An id is never reused. If a fact changes, the new wording becomes a new version. The old version stays here marked `superseded`, and the corrections log records the change.

## Sources

Facts and contacts point to sources by id. Each source is saved once to `.cache/sources/<source id>.<ext>`, with a plain-text copy at `.cache/sources/<source id>.txt` that the checkers read. The SHA-256 is of the saved original (HTML or PDF), not of the text copy.

- Source id form: `src-<owner>-<NN>`, in small letters, for example `src-rbi-01`. It never clashes with a fact id or a radar source id (S01).
- A "rendered copy" is the page as a browser shows it, saved because the site builds its text with JavaScript. Its SHA-256 is of that saved copy.

For rules, rights and deadlines, only primary sources count: the statute (indiacode.nic.in), the gazette (egazette.gov.in), or the regulator's own circular or page (for example rbi.org.in, sebi.gov.in, uidai.gov.in, dot.gov.in, i4c.mha.gov.in). G9 checks the domain.

| Source id | Title | Owner | URL | SHA-256 | Fetched |
|---|---|---|---|---|---|
| src-cybercrime-01 | National Cyber Crime Reporting Portal: Contact Us | I4C, MHA | https://cybercrime.gov.in/Webform/Crime_NodalGrivanceList.aspx | `43a5afb9bece875d05a708e2cf701e3bce06617246c56a509543aeb85774e444` | 30 Sep 2026 |
| src-mha-01 | MHA answer to Lok Sabha unstarred question 350, 22 July 2025 | MHA | https://www.mha.gov.in/MHA1/Par2017/pdfs/par2025-pdfs/LS22072025/350.pdf | `90eecb9dddb1dd09615c99c9dca383b5a0ca6d2271d48fede282d6468133b9b7` | 30 Sep 2026 |
| src-sancharsaathi-01 | Sanchar Saathi home page | DoT | https://sancharsaathi.gov.in | `e91a9f53cac73c5c8ef369054518f78fced1a91c2d5702da1cef6966bf6fe384` | 30 Sep 2026 |
| src-nch-01 | National Consumer Helpline: About | Department of Consumer Affairs | https://consumerhelpline.gov.in/public/about | `1a29b83985c7a12e3596c7bde34729cdd198e9264afb7b8b176d2f42864906a2` | 30 Sep 2026 |
| src-nalsa-01 | NALSA home page | NALSA | https://nalsa.gov.in | `1eb62f2e824a21b52ec0156e2c35da39820bedc7eaa872d45b78da7110556b8e` | 30 Sep 2026 |
| src-pib-01 | PIB release 2227723 (Ministry of Law and Justice, 13 Feb 2026): Tele-Law | Ministry of Law and Justice | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2227723&reg=3&lang=1 | `d57434432758e0f85b30207572ea61f350d637868c05722b5303c6a818947906` | 30 Sep 2026 |
| src-pgportal-01 | CPGRAMS: FAQ | DARPG | https://pgportal.gov.in/Home/Faq | `3dbdef89a2cb8a4f9f744af1880eca325ff58ff92f0c4608d7f2eecb0c2d42f3` | 30 Sep 2026 |
| src-rbi-01 | FAQ: Reserve Bank - Integrated Ombudsman Scheme, 2026 | RBI | https://www.rbi.org.in/commonman/Upload/English/FAQs/PDFs/RBIOS01072026.pdf | `db923b0fe96466e98510a151404c3022b5d8e3a48b51e304c142e354ba0dca66` | 30 Sep 2026 |
| src-rbi-02 | Reserve Bank - Integrated Ombudsman Scheme, 2026 (in force 1 July 2026), copy on RBI's complaint portal | RBI | https://cms.rbi.org.in/cms/assets/Documents/Ombudsman_Scheme_English.pdf | `1b3b438ca94721fde5dc27f37ce887b6579bcaf7f592ae297efaf7af150f5950` | 30 Sep 2026 |
| src-rbi-03 | RBI (Commercial Banks - Responsible Business Conduct) Third Amendment Directions, 2026, RBI/2026-27/167, 24 June 2026 | RBI | https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13543&Mode=0 | `92c56c3d80521fe006b508b451f9655d2242e7175263c00d7a69ab40b13577df` | 30 Sep 2026 |
| src-uidai-01 | UIDAI: CRM Division (grievance redressal) | UIDAI | https://uidai.gov.in/en/crm-division | `1458883b8fb2aaaf4ce5c8f239bb718bb2c44a2c40c3da1d6ec57f5ab0cbcac4` | 30 Sep 2026 |
| src-uidai-02 | UIDAI: Your Aadhaar (MyAadhaar portal) | UIDAI | https://uidai.gov.in/en/your-aadhaar | `a7a2ac50101a4fcee3e3d53f0ef239b005aa4b4a8e694bb0fcdaae72d867258f` | 30 Sep 2026 |
| src-experian-01 | Experian India: Consumer services | Experian Credit Information Company of India | https://www.experian.in/consumer/consumer-services/ | `853dedb28ab07113176dd0a2451046cf49114d207f3b072512fbdad7680b1a5e` | 30 Sep 2026 |
| src-equifax-01 | Equifax India: Consumer grievance redressal | Equifax Credit Information Services | https://www.equifax.co.in/support/consumer-grievance-redressal/ | `da01b5511f2d98a87fd3e6597393865af98d1f6fdb9faba6fab88f3e5a7df4f5` | 30 Sep 2026 |
| src-crif-01 | CRIF: Raise a dispute | CRIF Credit Information Services | https://www.crifhighmark.com/raise-a-dispute | `fda56d65e94bf184903364db210dddc5a969cb18c028081e1cbeb7ea0dce513c` | 30 Sep 2026 |
| src-whatsapp-01 | WhatsApp Help Center: How to use click to chat (rendered copy) | WhatsApp (Meta) | https://faq.whatsapp.com/5913398998672934/?locale=en_US | `499b9db23e9b971ca422d0360c08a0d971e93c47e0a03dea48023d8dedec9b20` | 30 Sep 2026 |
| src-egazette-01 | Gazette of India Extraordinary, 25 Dec 2023: The Bharatiya Nagarik Suraksha Sanhita, 2023 (No. 46 of 2023), as enacted | Ministry of Law and Justice (Legislative Department) | https://egazette.gov.in/WriteReadData/2023/250884.pdf | `5e60e2afe30d0fe7eca4f8126301146b76c86a444e690581f81eb564843517fe` | 30 Sep 2026 |
| src-mha-02 | MHA answer to Rajya Sabha unstarred question 553, Prevention of Cyber Financial Fraud, 4 Feb 2026 | MHA | https://www.mha.gov.in/MHA1/Par2017/pdfs/par2026-pdfs/RS04022026/553.pdf | `440ca59e134ff1d9ab1935b2a1b12c3b081ae719697e1e7abf831317348b5907` | 30 Sep 2026 |
| src-pib-02 | PIB release 2274249 (MHA, 17 Jun 2026): Home Minister reviews Helpline 1930 | MHA | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2274249&reg=48&lang=2 | `cb87ca9709e44f7931feefe9d2a2808339f104d220629e8713c169f4ce3e2a50` | 30 Sep 2026 |
| src-pib-03 | PIB release 2287674 (MHA, 22 Jul 2026): National Cybercrime Response Mechanism | MHA | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2287674&reg=48&lang=2 | `d309e5c7a530f9a8bc4caabf64194cc7f7a7e48286e16e73ae0b2715d3016cb8` | 30 Sep 2026 |
| src-mrm-01 | Money Restoration Portal: FAQ (rendered copy) | I4C, MHA | https://mrm-ncrp.mha.gov.in/public-info?tab=faq | `e57f5bdf2cd8073a03e7be66e3e5a12b79bf63cd1be50e40b56073e6003eb3a0` | 30 Sep 2026 |
| src-mrm-02 | Money Restoration Portal: How to Apply (rendered copy) | I4C, MHA | https://mrm-ncrp.mha.gov.in/public-info?tab=apply | `320dc68388fe32a470266f28a97ffec5f32a7ee22210205469c9e8f5e7dab932` | 30 Sep 2026 |
| src-mrm-03 | Money Restoration Portal: Raise Refund Request (rendered copy) | I4C, MHA | https://mrm-ncrp.mha.gov.in/raise-request | `d4096b52ba26907cfd3947626512b0a84e4e4fd2636e871b55f79fd4e656b58e` | 30 Sep 2026 |
| src-cyberdost-01 | CyberDost (I4C) Telegram post 4735, 31 Aug 2026: advisory on malicious adult-content Android apps | I4C, MHA (official Telegram channel) | https://t.me/cyberdosti4c/4735?embed=1&mode=tme | `b81cc0a09de0f034132001dc96319340c237d0a56d4958cc2c820d3b11d64f32` | 30 Sep 2026 |

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
- **open question:** (only when needed) what the source leaves unsettled. A page says it plainly or does not use the fact.
- **verified on / by:**
- **recheck by:** 180 days after verification for laws; 90 days for anything a regulator changes often
- **status:** candidate, verified, superseded, or rejected
- **version:** v1

## Facts

Nothing is verified yet. The blocks below are `candidate` (L02, 30 Sep 2026). Each quote was checked by script against the saved copy of its source.

**Group A. RBI liability rules for electronic banking fraud, transactions on or after 1 January 2027 (src-rbi-03).** These cover commercial banks other than small finance banks, payments banks, regional rural banks and local area banks. The rules for transactions before 1 January 2027 are not here yet (see the work queue).

### RBI-LIAB27-01

- **kind:** rule
- **statement.en:** These RBI rules apply to electronic banking transactions made on or after 1 January 2027.
- **conditions:** Only for customers of commercial banks other than small finance banks, payments banks, regional rural banks and local area banks (opening paragraph of the amendment). Other bank types have their own amendments, not saved yet (STATE.md, known issue K12).
- **applies to:** all
- **source:** src-rbi-03, paragraph 3(2)
- **quote:** "(2) These Directions shall apply in cases of electronic banking transactions undertaken by customers of a bank on or after January 1, 2027."
- **open question:** The amendment does not say in words which rules cover transactions before 1 January 2027.
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-02

- **kind:** rule
- **statement.en:** A fraudulent transaction is one made by someone else using your payment details that they got from you by fraud. It is also one you approved yourself because someone forced or threatened you.
- **conditions:** The same definition also covers any unauthorised transaction (RBI-LIAB27-03). An electronic banking transaction means an "electronic funds transfer" under Section 2(c) of the Payment and Settlement Systems Act, 2007, and includes card present and card not present transactions (new paragraph 4(10D)).
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, new paragraph 4(15A)
- **quote:** "Fraudulent electronic banking transaction (Fraudulent EBT) means an EBT executed by a third-party using the credentials obtained from the customer through fraudulent means or executed by the customer by granting approval under coercion or duress from the third-party"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-03

- **kind:** rule
- **statement.en:** An unauthorised transaction is one you did not authorise. It includes one caused by the bank's negligence or by a fault somewhere else in the system.
- **conditions:** "Inter alia": the list is not complete. "A fault somewhere else in the system" is the source's "third-party breach" (RBI-LIAB27-08). The definition of a fraudulent transaction includes every unauthorised transaction (new paragraph 4(15A), see RBI-LIAB27-02).
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, new paragraph 4(26B)
- **quote:** "Unauthorised electronic banking transaction (Unauthorised EBT) means an EBT which is not authorised by a customer and inter alia includes an EBT occurring on account of negligence by a bank and / or a third-party breach."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-04

- **kind:** right
- **statement.en:** If the fraud happened because of the bank's negligence or fault, you pay nothing and the bank must reverse the transaction. This is so even if you did not report it.
- **conditions:** What counts as the bank's negligence: RBI-LIAB27-05 to 07.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76L
- **quote:** "entitled to zero liability and reversal of the transaction in cases where the fraudulent EBT occurs due to negligence / deficiency on the part of the bank, irrespective of whether the transaction is reported by the customer or not."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-05

- **kind:** rule
- **statement.en:** The bank is negligent if, among other things, it has not put in place the safety systems it must have, or has not sent the alerts it must send.
- **conditions:** The list is open ("inter alia"). The other items are in RBI-LIAB27-06 and 07.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, new paragraph 4(20B), items (i) and (ii)
- **quote:** "Negligence by a bank inter alia includes the following actions by the bank: (i) not putting in place the mandated systems and procedures to ensure safety and security of EBTs; or (ii) not sending mandatory alerts for EBTs; or"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-06

- **kind:** rule
- **statement.en:** The bank is also negligent if it does not give you a way to report fraud or a lost card at any hour on any day, or does not act with care on your report.
- **conditions:** Part of the open list in new paragraph 4(20B), which begins "Negligence by a bank inter alia includes the following actions by the bank".
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, new paragraph 4(20B), items (iii) and (iv)
- **quote:** "(iii) not providing 24x7 channels for reporting of fraudulent EBTs or loss of debit / credit card; or (iv) not acting diligently upon a customer notification regarding unauthorised EBT(s) or loss of debit / credit card; or"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-07

- **kind:** rule
- **statement.en:** The bank is also negligent if a system failure, a security breach or a fraud inside the bank led to the transaction.
- **conditions:** Part of the open list in new paragraph 4(20B).
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, new paragraph 4(20B), item (v)
- **quote:** "(v) system malfunctions / security breaches / internal frauds leading to unauthorised EBTs."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-08

- **kind:** rule
- **statement.en:** A third-party breach is when the fault lies neither with the bank nor with you, but somewhere else in the system.
- **conditions:** Examples of "somewhere else": RBI-LIAB27-09.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, new paragraph 4(26.1A)
- **quote:** "Third-party breach means a situation where the deficiency lies neither with the bank nor with the customer but lies elsewhere in the system"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-09

- **kind:** rule
- **statement.en:** This includes a fault at a go-between such as a third-party application provider, a payment aggregator, a payment gateway or a telecom company.
- **conditions:** "Such as ... etc.": the list is not complete. The source does not define "third-party application provider".
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, new paragraph 4(26.1A)
- **quote:** "lies elsewhere in the system and includes deficiency on the part of an intermediary such as a Third-Party Application Provider (TPAP), Payment Aggregator (PA), Payment Gateway (PG), Telecom Service Provider (TSP), etc."
- **open question:** The source does not name SIM swap or any other scam type. Whether a telecom company's SIM swap lapse counts is a reading of the text, not the text.
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-10

- **kind:** deadline
- **statement.en:** If the fault lies somewhere else in the system, and you report the transaction to your bank within 5 calendar days of the day it happened, you pay nothing and the bank must reverse it.
- **conditions:** Calendar days, not working days. Counted from the date of the transaction, not from the bank's alert. The report must reach the bank itself. Only for a third-party breach (RBI-LIAB27-08).
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76M
- **quote:** "A customer shall be entitled to zero liability and reversal of the transaction in cases of third-party breach where the customer reports the unauthorised fraudulent EBT to the bank within five calendar days from the date of its occurrence."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-11

- **kind:** rule
- **statement.en:** If the fault lies somewhere else in the system and you report it to the bank after 5 calendar days, the bank's own policy decides how much you pay.
- **conditions:** Only for a third-party breach (RBI-LIAB27-08). The bank may also waive your liability at its discretion (paragraph 76P).
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76M
- **quote:** "In cases of third-party breach reported to the bank after five calendar days, the customer’s liability shall be determined as per the bank’s policy."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-12

- **kind:** rule
- **statement.en:** If the fraud happened because you were careless, you are liable for the loss, except the part that the small-value compensation covers.
- **conditions:** Only until you report the fraud to the bank: the paragraph ends "until he / she reports the fraudulent EBT to the bank". Losses after your report: RBI-LIAB27-17. What counts as your negligence: RBI-LIAB27-13 to 16. The compensation: RBI-LIAB27-22 to 27.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76N
- **quote:** "negligence by the customer, he / she shall be liable for the loss incurred by him / her, to the extent of loss not eligible for compensation as per the mechanism detailed at paragraph 76T below,"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-13

- **kind:** rule
- **statement.en:** Your negligence includes not taking reasonable care of your PIN, password, OTP or other details. One example is giving them to another person to make a transaction, whether you meant to or not.
- **conditions:** Part of the open list in new paragraph 4(20C), which begins "Negligence by a customer inter alia includes the following actions by the customer". The source gives a second example: writing down and storing the PIN with a debit or credit card.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, new paragraph 4(20C), item (i)
- **quote:** "(i) failing to exercise reasonable care in usage of credentials such as PIN, password, OTP or other details (e.g., providing credentials for carrying out transactions to another person, whether intentionally or otherwise"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-14

- **kind:** rule
- **statement.en:** Your negligence also includes not telling the bank promptly after you find out about a fraud or lose your debit or credit card.
- **conditions:** Part of the open list in new paragraph 4(20C).
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, new paragraph 4(20C), item (ii)
- **quote:** "(ii) not notifying the bank promptly after finding out about a fraudulent EBT, or loss of a debit / credit card; or"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-15

- **kind:** rule
- **statement.en:** Your negligence also includes not paying attention to a specific and clear warning from the bank, meant for you, that a payment you are about to make is likely a scam.
- **conditions:** Part of the open list in new paragraph 4(20C).
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, new paragraph 4(20C), item (iii)
- **quote:** "(iii) not paying attention to specific, directed and clear warnings from the bank that a prospective transaction is likely a scam; or"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-16

- **kind:** rule
- **statement.en:** Your negligence also includes downloading harmful apps, and not updating your mobile number or email address with the bank when it changes.
- **conditions:** Part of the open list in new paragraph 4(20C).
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, new paragraph 4(20C), items (iv) and (v)
- **quote:** "(iv) downloading malicious apps; or (v) failing to update her / his registered mobile number / email address with the bank in case of change."
- **open question:** "Malicious apps" is not defined. Seed card 1 (sideloaded apps) must use this fact with care.
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-17

- **kind:** rule
- **statement.en:** Any loss from unauthorised transactions made after you report the fraud to the bank is the bank's to bear.
- **conditions:** Counted from your report to the bank.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76O
- **quote:** "Loss arising from any unauthorised transaction occurring after the reporting of the fraudulent EBT by a customer to a bank shall be borne by the bank."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-18

- **kind:** rule
- **statement.en:** It is for the bank to prove that you are liable.
- **conditions:** For complaints about fraudulent transactions.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76K
- **quote:** "The burden of proving customer liability in complaints involving fraudulent EBTs shall lie on the bank."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-19

- **kind:** deadline
- **statement.en:** For a fraud inside India, the time in the bank's policy cannot be more than 45 calendar days from the day the bank got your complaint.
- **conditions:** "This timeline" is the time in the bank's policy within which it examines the complaint, establishes liability and replies, as applicable (RBI-LIAB27-32). For a fraud across borders the most is 60 calendar days. If you pay nothing (RBI-LIAB27-04 or 10), the reply must include the details of the reversal. If the loss came from your negligence, the reply must include the compensation details in eligible cases.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76Q
- **quote:** "this timeline shall not exceed 45 calendar days from the date of receipt of the complaint by the bank in case of a complaint arising out of domestic fraudulent EBT(s)"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-32

- **kind:** process
- **statement.en:** The bank must examine your fraud complaint, decide who is liable, and reply to you as applicable, within the time set in its policy.
- **conditions:** The longest time the policy may set: RBI-LIAB27-19. What the reply must include: RBI-LIAB27-19, conditions.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76Q, first sentence
- **quote:** "A bank shall ensure that a complaint arising out of fraudulent EBT(s) is examined, liability therein is established and response, as applicable, is issued to the customer within such time as may be specified in the bank’s policy."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-20

- **kind:** deadline
- **statement.en:** For a fraud on your credit card, the bank must give you a temporary credit of the amount within 5 calendar days of your report.
- **conditions:** Credit cards only. The temporary credit cannot be used (RBI-LIAB27-21).
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76R
- **quote:** "fraudulent EBT(s) in a credit card, a bank shall provide shadow reversal equivalent to the amount involved in the fraudulent EBT(s) within five calendar days from the date of receipt of notification"
- **open question:** The new rules set no temporary-credit deadline for bank accounts or debit cards.
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-21

- **kind:** rule
- **statement.en:** You cannot use this temporary credit, and you do not pay extra interest or charges on it.
- **conditions:** The source calls it a "shadow reversal": a temporary credit before the bank's investigation or any insurance claim is settled.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, new paragraph 4(25A)
- **quote:** "While the customer shall not be allowed to use such amount, he / she will not bear any additional burden of interest / charges."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-22

- **kind:** amount
- **statement.en:** You can get compensation of 85% of your net loss or ₹25,000, whichever is less. You can get it only once in your lifetime.
- **conditions:** Net loss is the gross loss minus any money recovered, before or after the compensation is paid. Only when RBI-LIAB27-23 and 24 are met. Only for frauds up to one year from the effective date of the rules (RBI-LIAB27-27). For a joint account, only one holder may claim; claiming as a joint holder bars a later claim as a single holder, and the other way round (Explanation to paragraph 76T(1)).
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76T(1)
- **quote:** "shall be compensated 85 per cent of the net loss amount (calculated after reducing recoveries made, whether before or after paying the compensation, from the gross loss amount), or ₹25,000, whichever is less, once during her / his lifetime"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-23

- **kind:** rule
- **statement.en:** This compensation is for a genuine victim who is an individual, including a sole proprietor, who has made a complaint about a total loss of ₹50,000 or less, where the loss came from their own negligence.
- **conditions:** The bank must find the loss genuine under its own policy (paragraph 76T(1)(a)). The victim must also report in time (RBI-LIAB27-24). Only for frauds up to one year from the effective date (RBI-LIAB27-27). Only once in a lifetime, and only one holder of a joint account may claim (RBI-LIAB27-22). "Their own negligence" is the source's reference to paragraph 76N (RBI-LIAB27-12).
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76T(1)
- **quote:** "A bona fide victim, being an individual person, including a sole proprietor, and having lodged a complaint involving gross loss of an amount up to ₹50,000 on account of fraudulent EBT(s) covered under paragraph 76N above"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-24

- **kind:** deadline
- **statement.en:** To get this compensation, report the fraud in both places within 5 calendar days of the day it happened: on the National Cyber Crime Reporting Portal or the National Cyber Crime Helpline, and to your bank.
- **conditions:** Both reports are needed. Calendar days, counted from the date of the transaction.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76T(1)(b)
- **quote:** "(b) the victim has reported the fraudulent EBT(s) on the National Cyber Crime Reporting Portal or National Cyber Crime Helpline (1930) and to the bank within five calendar days from its occurrence."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-25

- **kind:** process
- **statement.en:** If the bank finds your complaint genuine, it must give you a form to claim this compensation.
- **conditions:** After the bank's examination under paragraph 76Q (RBI-LIAB27-19).
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76T(4)
- **quote:** "where the customer’s bank is satisfied that the complaint is bona fide, it shall provide the customer an application form as per the format provided at Annex II(1) to claim compensation for the loss suffered by her / him."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-26

- **kind:** deadline
- **statement.en:** The bank must pay the compensation within 5 calendar days of getting your filled form.
- **conditions:** Counted from the bank's receipt of your application.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76T(5)
- **quote:** "The customer’s bank shall, within five calendar days of receipt of the application from a customer, compensate the customer as given above."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-27

- **kind:** rule
- **statement.en:** This compensation is paid only for frauds that happen up to one year from the date these rules take effect.
- **conditions:** None stated beyond the quote.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76U
- **quote:** "The compensation shall be payable for losses incurred on fraudulent EBTs occurring up to one year from the effective date of these Directions."
- **open question:** "Effective date" is not defined. Paragraph 3(2) applies the rules to transactions on or after 1 January 2027, but does not call that the effective date.
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-28

- **kind:** right
- **statement.en:** If the bank rejects your complaint and holds you liable, it must tell you why and give you the supporting details, if any.
- **conditions:** "Rejected" means the bank found you liable.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76S
- **quote:** "In case of rejected complaints, i.e., in cases where customer liability is established, a bank shall disclose the reason for such rejection and with the supporting details, if any, to the customer."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-29

- **kind:** process
- **statement.en:** When you report a fraud, the bank must at once send you an acknowledgement with the complaint number and the date and time it got your complaint.
- **conditions:** The bank registers your report as a complaint. The acknowledgement may come by SMS, email or in the app.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76I
- **quote:** "sends an immediate acknowledgement to the customer, along with the complaint number and the date and time of receipt of the complaint"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-30

- **kind:** process
- **statement.en:** The bank's transaction SMS must give a number that you can send an SMS to at once, to object to the transaction.
- **conditions:** One of the reporting channels the bank must give (paragraph 76G).
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76G(2)
- **quote:** "provide a number in the transaction alert SMS itself, to which the customer can immediately send an SMS to notify her / his objection, if any; and"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-LIAB27-31

- **kind:** process
- **statement.en:** Once you report the fraud, the bank must act promptly to stop more unauthorised transactions in your accounts, and tell you what it did.
- **conditions:** "Under advice to him / her": the bank must tell you.
- **applies to:** all; scope as in RBI-LIAB27-01 (transactions on or after 1 January 2027, at the banks named there)
- **source:** src-rbi-03, paragraph 76J
- **quote:** "On receipt of a complaint regarding any fraudulent EBT from a customer, a bank shall take prompt steps to prevent further unauthorised EBTs in the customer’s account(s) under advice to him / her."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

**Group B. RBI Ombudsman, Reserve Bank - Integrated Ombudsman Scheme, 2026 (src-rbi-02).** In force from 1 July 2026. It repealed the 2021 Scheme; complaints received before 1 July 2026 stay under the 2021 Scheme (clause 20).

### RBI-OMB-01

- **kind:** right
- **statement.en:** If something your bank did, or failed to do, gave you poor service, you can complain to the RBI Ombudsman yourself or through someone you authorise.
- **conditions:** "Deficiency in service" means a shortcoming in any service the bank must give, whether or not you lost money (clause 3(1)(i)). An authorised representative must be a person other than an advocate, "duly appointed and authorised in writing" (clause 3(1)(c)). The Scheme covers commercial banks, regional rural banks, state and central co-operative banks, scheduled urban co-operative banks, non-scheduled urban co-operative banks with deposits of ₹50 crore or more (clause 1(3)(a)), some NBFCs (clause 1(3)(b)), non-bank prepaid payment instrument issuers (clause 1(3)(c)) and credit information companies (clause 1(3)(d)). It does not cover a bank in resolution or winding up, or under All-Inclusive Directions (clause 3(1)(e)). A complaint is maintainable only if every condition in clause 10(1) is met: (a) addressed to the Ombudsman directly (RBI-OMB-06); (b) no advocate as representative (RBI-OMB-07); (c) complete information as in clause 11; (d) not abusive, frivolous or vexatious; (e) complained to the bank first (RBI-OMB-02); (f) no reply in time or not satisfied (RBI-OMB-03, 04); (g) within 90 days (RBI-OMB-05); (h), (i) not already pending before, or decided by, the Ombudsman; (j), (k) not pending before, or decided by, a court or similar forum (RBI-OMB-09); (l) the complaint to the bank was made within the period of limitation under the Limitation Act, 1963. Clause 10(2) excludes some matters, for example a bank's commercial judgment, and an action the bank took on the order of a court or a law enforcing authority.
- **applies to:** all; complaints to the Ombudsman received on or after 1 July 2026 (clause 20)
- **source:** src-rbi-02, clause 9
- **quote:** "Any customer aggrieved by an act or omission of a Regulated Entity resulting in deficiency in service may file a complaint under the Scheme personally or through an authorised representative as defined under clause 3(1)(c)."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-OMB-02

- **kind:** rule
- **statement.en:** Before you go to the Ombudsman, you must first complain to your bank, in writing or another way, and be able to show proof that you did.
- **conditions:** A complaint that does not meet this is rejected at the start (clause 10(3)).
- **applies to:** all; complaints to the Ombudsman received on or after 1 July 2026 (clause 20)
- **source:** src-rbi-02, clause 10(1)(e)
- **quote:** "the Complainant had first made a complaint in writing or through any other mode to the Regulated Entity concerned, where proof of having made a complaint can be produced by the Complainant, before making a complaint under the Scheme"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-OMB-03

- **kind:** deadline
- **statement.en:** One condition for going to the Ombudsman is met if your bank has not replied within 30 days, or within the time set by RBI, NPCI or card network rules if that is longer. The time counts from when the bank got your complaint.
- **conditions:** Counted from the bank's receipt of your complaint. "Whichever is higher" in clause 10(1)(f). This is one of the clause 10(1) conditions, and every one of them must be met (listed under RBI-OMB-01). The clause 10(2) exclusions also apply.
- **applies to:** all; complaints to the Ombudsman received on or after 1 July 2026 (clause 20)
- **source:** src-rbi-02, clause 10(1)(f)
- **quote:** "has not received any reply within 30 days or within the time specified by the Reserve Bank, National Payments Corporation of India, or under Card Network guidelines, if any, whichever is higher after the Regulated Entity received the complaint"
- **open question:** The Scheme and its FAQ do not say whether "the time specified by the Reserve Bank" includes the 45-day limit for fraud complaints (RBI-LIAB27-19). If it does, a fraud victim with no reply may have to wait that long. The Scheme's Annex says "whichever is later". Do not state a wait for fraud cases until this is settled.
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-OMB-04

- **kind:** right
- **statement.en:** The same condition is also met if your bank has replied and you are not satisfied with the reply.
- **conditions:** This is one of the clause 10(1) conditions, and every one of them must be met (listed under RBI-OMB-01). The clause 10(2) exclusions also apply.
- **applies to:** all; complaints to the Ombudsman received on or after 1 July 2026 (clause 20)
- **source:** src-rbi-02, clause 10(1)(f)
- **quote:** "or the Complainant is not satisfied with the reply / resolution provided by the Regulated Entity"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-OMB-05

- **kind:** deadline
- **statement.en:** Complain to the Ombudsman within 90 days. Count from the end of the waiting time in RBI-OMB-03, or from the date of the last message from your bank, whichever is later.
- **conditions:** One of the clause 10(1) conditions (listed under RBI-OMB-01).
- **applies to:** all; complaints to the Ombudsman received on or after 1 July 2026 (clause 20)
- **source:** src-rbi-02, clause 10(1)(g)
- **quote:** "the complaint is made to the RBI Ombudsman within 90 days from the date on which the timeline specified in sub-clause (1)(f) expires or the date of the last communication from the concerned Regulated Entity, whichever is later"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-OMB-06

- **kind:** rule
- **statement.en:** Send your complaint to the RBI Ombudsman directly. Only marking a copy to RBI on your email or letter to the bank does not count.
- **conditions:** By email or on paper, the same rule applies.
- **applies to:** all; complaints to the Ombudsman received on or after 1 July 2026 (clause 20)
- **source:** src-rbi-02, clause 10(1)(a)
- **quote:** "the complaint is addressed to the RBI Ombudsman directly. However, it does not include a communication in which the Reserve Bank is merely endorsed/marked in copy (whether by e-mail or in physical form)"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-OMB-07

- **kind:** rule
- **statement.en:** You can complain yourself or through someone you authorise, but that person cannot be a lawyer, unless the lawyer is the person who was wronged.
- **conditions:** The representative must be "duly appointed and authorised in writing" by you (clause 3(1)(c)).
- **applies to:** all; complaints to the Ombudsman received on or after 1 July 2026 (clause 20)
- **source:** src-rbi-02, clause 10(1)(b)
- **quote:** "the complaint is lodged by the Complainant personally or through an authorised representative other than an advocate unless the advocate is the aggrieved person"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-OMB-08

- **kind:** rule
- **statement.en:** For the rule in RBI-OMB-09, a criminal case or a police investigation about the matter does not count as the same grievance.
- **conditions:** Only "for the purposes of sub-clause (1)(j) and (1)(k)" (the opening words of the Explanation). Separately, clause 16(1)(c) lets the Ombudsman reject a complaint at any stage if a case on the same cause of action is filed before a court, tribunal, arbitrator or similar forum while the complaint is being examined; the Explanation does not cover clause 16.
- **applies to:** all; complaints to the Ombudsman received on or after 1 July 2026 (clause 20)
- **source:** src-rbi-02, clause 10(1), Explanation 1
- **quote:** "a complaint relating to the same grievance does not include criminal proceedings pending or decided before a Court or Tribunal or any police investigation initiated in a criminal offence."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-OMB-09

- **kind:** rule
- **statement.en:** You cannot go to the Ombudsman if the same grievance is already before a court, a tribunal, an arbitrator or a similar forum.
- **conditions:** This holds "whether or not received from the same Complainant or along with one or more of the Complainants" (the words after the quote). The same applies if such a forum has already settled or decided it on merits (clause 10(1)(k)). A criminal case or a police investigation does not count as the same grievance (Explanation 1, RBI-OMB-08).
- **applies to:** all; complaints to the Ombudsman received on or after 1 July 2026 (clause 20)
- **source:** src-rbi-02, clause 10(1)(j)
- **quote:** "the complaint is not relating to the same grievance, which is already pending before any Court, Tribunal or Arbitrator or any other judicial or quasi-judicial forum"
- **open question:** The Scheme does not say whether a consumer commission counts as a "quasi-judicial forum". Do not name one on a page without a source.
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### RBI-OMB-10

- **kind:** process
- **statement.en:** You can complain to the RBI Ombudsman in three ways: online on RBI's complaint portal, by email, or by post or courier with the complaint form and your documents.
- **conditions:** The portal is contact C05 and the email is contact C20. The postal address is in the source (Annex, Part A, item 6). A complaint on paper must be signed by you or your authorised representative (clause 11(2)).
- **applies to:** all; complaints to the Ombudsman received on or after 1 July 2026 (clause 20)
- **source:** src-rbi-02, Annex, Part A, item 6
- **quote:** "(i) through the online CMS portal at https://cms.rbi.org.in ; (ii) or by emailing to: crpc@rbi.org.in; or (iii) by sending a filled-in complaint form with supporting documents by post/courier to the following address:"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

**Group C. Reporting fast, and getting held money back (src-mha-02, src-pib-02, src-pib-03, src-mrm-01 to 03).** No official text found gives a national time window such as a "golden hour". The pages must not state one.

### I4C-REPORT-01

- **kind:** office
- **statement.en:** I4C runs the Citizen Financial Cyber Fraud Reporting and Management System. It is for reporting financial fraud at once, and for stopping fraudsters from moving the money away.
- **conditions:** Financial fraud only. The source states the purpose; it gives no time limit and promises no result.
- **applies to:** all
- **source:** src-mha-02, answer, item ii
- **quote:** "The ‘Citizen Financial Cyber Fraud Reporting and Management System’ (CFCFRMS), under I4C, has been launched in year 2021 for immediate reporting of financial frauds and to stop siphoning off funds by the fraudsters."
- **verified on / by:**
- **recheck by:** 180 days after verification
- **status:** candidate
- **version:** v1

### I4C-REPORT-02

- **kind:** process
- **statement.en:** The reporting system helps block fraud transactions promptly through the banking network. This raises the chance that the money can be secured and returned to victims.
- **conditions:** "Possibility" only. Nothing is promised.
- **applies to:** all
- **source:** src-pib-02, paragraph on the reporting system
- **quote:** "The system helps in promptly blocking fraudulent financial transactions through the banking network, thereby increasing the possibility of securing and restoring funds to victims."
- **open question:** The source is a press release about a review meeting, not a rule. It gives no time window.
- **verified on / by:**
- **recheck by:** 180 days after verification
- **status:** candidate
- **version:** v1

### I4C-MRM-01

- **kind:** office
- **statement.en:** The Money Restoration Module is for returning defrauded money to victims quickly.
- **conditions:** The same sentence says it was made functional from April 2026.
- **applies to:** all
- **source:** src-pib-03, paragraph on NCRP modules
- **quote:** "Money Restoration Module for expeditious restoration of defrauded money to the victims"
- **verified on / by:**
- **recheck by:** 180 days after verification
- **status:** candidate
- **version:** v1

### I4C-MRM-02

- **kind:** process
- **statement.en:** When money is held against your complaint, you get an SMS that says so. After the date given in that SMS, you log in to the Money Restoration Portal.
- **conditions:** An amount must be "provisionally held" against your complaint. Log in only after the date in the SMS. The portal is contact C04. The same sentence goes on: the victim "applies for interim custody" through the module (steps in I4C-MRM-04 to 06).
- **applies to:** all
- **source:** src-mrm-01, question 2
- **quote:** "The victim logs in to the Money Restoration Portal (MRM) https://mrm-ncrp.mha.gov.in, after the date mentioned in the SMS, which confirms an amount has been provisionally held against their complaint,"
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### I4C-MRM-03

- **kind:** process
- **statement.en:** Once the money is put on hold, the bank works out how much of it can be returned.
- **conditions:** The bank follows the Standard Operating Procedure (SOP). No official copy of the SOP was found on 30 Sep 2026. The FAQ then lists an SMS, an email and a portal link as the notices you get.
- **applies to:** all
- **source:** src-mrm-01, question 1
- **quote:** "Once the amount is put on hold, the bank analyses the hold as per SOP and determines the restorable amount."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### I4C-MRM-04

- **kind:** process
- **statement.en:** On the portal, choose "Raise Refund Request", enter the 14-digit acknowledgement number you got when your complaint was registered, and verify the OTP.
- **conditions:** The source calls it the "NCRP Acknowledgement ID": the number from the National Cyber Crime Reporting Portal.
- **applies to:** all
- **source:** src-mrm-02, step 1
- **quote:** "Click on “Raise Refund Request” tab, enter the 14 digit NCRP Acknowledgement ID received at the time of complaint registration and verify the OTP."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### I4C-MRM-05

- **kind:** process
- **statement.en:** You must give the correct details of the bank account where the money should be paid back.
- **conditions:** The same step says you can upload a court order if you have one.
- **applies to:** all
- **source:** src-mrm-02, step 2
- **quote:** "The victim must enter the correct account details of the respective banks, where the refunded amount will be credited."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### I4C-MRM-06

- **kind:** process
- **statement.en:** You must sign an indemnity bond on the portal and give a copy of your PAN card. The bond is a promise to bring the money to court when asked and to follow the court's orders.
- **conditions:** The money is given to you in custody; the court may still pass orders on it.
- **applies to:** all
- **source:** src-mrm-01, question 6
- **quote:** "The victim executes an indemnity bond — an undertaking to produce the amount before the court when required and to comply with the court's further orders, and a PAN card copy on MRM."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### I4C-MRM-07

- **kind:** rule
- **statement.en:** In a complaint, if the amount held in one bank is below ₹50,000, the money can be returned on police instructions without an FIR.
- **conditions:** Counted within a given complaint, for each bank. "Subject to the conditions prescribed in the SOP"; no official copy of the SOP was found on 30 Sep 2026.
- **applies to:** all
- **source:** src-mrm-01, question 4
- **quote:** "In a given complaint, where the amount put on hold in a given bank is below ₹50,000, restoration through the police instructions may proceed without FIR requirements, subject to the conditions prescribed in the SOP."
- **open question:** The FAQ says "bank" here and "bank account" in I4C-MRM-08, and neither covers exactly ₹50,000.
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### I4C-MRM-08

- **kind:** rule
- **statement.en:** If the amount held in one bank account is more than ₹50,000, an FIR is needed before the money can be returned.
- **conditions:** Counted for each bank account.
- **applies to:** all
- **source:** src-mrm-01, question 4
- **quote:** "where the amount put on hold in a given bank account exceeds ₹50,000, FIR requirements become mandatory for undertaking restoration."
- **open question:** Same as I4C-MRM-07.
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### I4C-MRM-09

- **kind:** deadline
- **statement.en:** After the police investigating officer orders it, the bank gives you custody of the held money within 15 calendar days.
- **conditions:** The order is under section 106(3) of the Bharatiya Nagarik Suraksha Sanhita, 2023. The bank finds your account from the reporting system. The FAQ (question 9) says a bank that does not comply records the reasons for not complying.
- **applies to:** all
- **source:** src-mrm-01, question 8
- **quote:** "On the IO's order under S.106(3) BNSS, the bank gives custody of the disputed amount to the victim — ascertaining the victim's account from CFCFRMS — within 15 calendar days, and updates the release on NCRP."
- **open question:** This is FAQ wording, not the SOP.
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### I4C-MRM-10

- **kind:** advisory
- **statement.en:** Do not deal with any middleman or agent. Use the official portal to track your application. For help, contact your police station.
- **conditions:** None.
- **applies to:** all
- **source:** src-mrm-03, "Public Advisory"
- **quote:** "Citizens are advised not to engage with any middlemen or agents (dalals). Please use the official portal to track application status. For assistance, contact your concerned Police Station."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

**Group D. Zero FIR: giving information to any police station (src-egazette-01).** The source is the Act as enacted in the Gazette. India Code, which shows later amendments, returned HTTP 504 on 30 Sep 2026, so amendments are not checked yet. The words "Zero FIR" are not in the Act.

### BNSS-ZEROFIR-01

- **kind:** right
- **statement.en:** You can give information about a cognizable offence to the officer in charge of any police station, even if the offence happened in another area. You can give it by speaking or electronically.
- **conditions:** Cognizable offences only. Given to the officer in charge of a police station.
- **applies to:** all
- **source:** src-egazette-01, section 173(1)
- **quote:** "Every information relating to the commission of a cognizable offence, irrespective of the area where the offence is committed, may be given orally or by electronic communication to an officer in charge of a police station, and if given—"
- **open question:** Whether a given cyber fraud is a cognizable offence is not in this section. It needs the Bharatiya Nyaya Sanhita and the First Schedule, which are not checked yet.
- **verified on / by:**
- **recheck by:** 180 days after verification
- **status:** candidate
- **version:** v1

### BNSS-ZEROFIR-02

- **kind:** rule
- **statement.en:** If you give the information by speaking, the officer must write it down, or have it written down, and read it back to you.
- **conditions:** Section 173(1)(i). The provisos to section 173(1) add rules for some offences under the Bharatiya Nyaya Sanhita, 2023 (sections 64 to 71, 74 to 79 and 124): the information of a woman victim is recorded by a woman officer; for a disabled person, it is recorded at home or a place of their choice, with an interpreter or special educator, and videographed, and the police get the person's statement recorded by a Magistrate as soon as possible.
- **applies to:** all
- **source:** src-egazette-01, section 173(1)(i)
- **quote:** "(i) orally, it shall be reduced to writing by him or under his direction, and be read over to the informant;"
- **verified on / by:**
- **recheck by:** 180 days after verification
- **status:** candidate
- **version:** v1

### BNSS-ZEROFIR-03

- **kind:** rule
- **statement.en:** You must sign the information, whether you gave it in writing or the officer wrote it down.
- **conditions:** Section 173(1)(i).
- **applies to:** all
- **source:** src-egazette-01, section 173(1)(i)
- **quote:** "and every such information, whether given in writing or reduced to writing as aforesaid, shall be signed by the person giving it;"
- **verified on / by:**
- **recheck by:** 180 days after verification
- **status:** candidate
- **version:** v1

### BNSS-ZEROFIR-04

- **kind:** deadline
- **statement.en:** If you give the information electronically, it is taken on record when you sign it within three days.
- **conditions:** Signed by the person who gave it. Its substance is then entered in the station's book, in the form the State Government prescribes. The provisos to section 173(1) on who records and how apply here too (see BNSS-ZEROFIR-02).
- **applies to:** all
- **source:** src-egazette-01, section 173(1)(ii)
- **quote:** "(ii) by electronic communication, it shall be taken on record by him on being signed within three days by the person giving it,"
- **open question:** The Act does not say how to sign, or what happens if you do not sign within three days.
- **verified on / by:**
- **recheck by:** 180 days after verification
- **status:** candidate
- **version:** v1

### BNSS-ZEROFIR-05

- **kind:** right
- **statement.en:** You must be given a copy of the information as recorded, at once and free of cost.
- **conditions:** Given to the informant or the victim.
- **applies to:** all
- **source:** src-egazette-01, section 173(2)
- **quote:** "(2) A copy of the information as recorded under sub-section (1) shall be given forthwith, free of cost, to the informant or the victim."
- **verified on / by:**
- **recheck by:** 180 days after verification
- **status:** candidate
- **version:** v1

### BNSS-ZEROFIR-06

- **kind:** right
- **statement.en:** If the police station refuses to record your information, you can send it in writing, by post, to the Superintendent of Police.
- **conditions:** The officer in charge must have refused. If satisfied that it discloses a cognizable offence, the Superintendent of Police investigates or directs an investigation. Only if that fails ("failing which") may you apply to the Magistrate.
- **applies to:** all
- **source:** src-egazette-01, section 173(4)
- **quote:** "refusal on the part of an officer in charge of a police station to record the information referred to in sub-section (1), may send the substance of such information, in writing and by post, to the Superintendent of Police concerned"
- **verified on / by:**
- **recheck by:** 180 days after verification
- **status:** candidate
- **version:** v1

**Group E. Seed card 1: sideloaded adult-content apps (src-cyberdost-01).** The advisory PDF is on i4c.mha.gov.in, which did not answer on 30 Sep 2026 (known issue K9). These blocks come from I4C's own CyberDost Telegram channel, which is not a government domain. Satya decides whether that source is enough, or whether the card waits for the PDF.

### I4C-ADV-2026-08-01

- **kind:** advisory
- **statement.en:** I4C has warned about harmful Android apps that pretend to be adult-content apps. They are promoted through advertisements on social media.
- **conditions:** Android only.
- **applies to:** all
- **source:** src-cyberdost-01, post text
- **quote:** "I4C, Ministry of Home Affairs, has cautioned citizens against malicious Android apps disguised as adult-content apps and promoted through advertisements on social media platforms."
- **open question:** The post is dated 31 August 2026. The advisory date (26 August 2026 in rules/taxonomy.md) is not in any saved official text.
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

### I4C-ADV-2026-08-02

- **kind:** advisory
- **statement.en:** These apps use names such as "Night Play", "Reloop", "Kyss", "Vimo", "Rivo", "Nexo" and "Vixa", and similar names. They may send you to websites that ask you to download an APK file from outside the official app stores.
- **conditions:** "May"; "along with similar variants".
- **applies to:** all
- **source:** src-cyberdost-01, post text
- **quote:** "Apps operating under names such as “Night Play”, “Reloop”, “Kyss”, “Vimo”, “Rivo”, “Nexo” and “Vixa”, along with similar variants, may redirect users to websites that prompt them to download APK files from outside official app stores."
- **open question:** App names change fast. A page that lists them needs a short recheck date.
- **verified on / by:**
- **recheck by:** 30 days after verification
- **status:** candidate
- **version:** v1

### I4C-ADV-2026-08-03

- **kind:** advisory
- **statement.en:** Once installed, these apps may misuse the Accessibility permission and take control of your phone. This can lead to payments you did not allow.
- **conditions:** "May"; "potentially". Accessibility is the only permission the post names.
- **applies to:** all
- **source:** src-cyberdost-01, post text
- **quote:** "Once installed, such apps may misuse Accessibility permissions, take control of the device and potentially enable unauthorised financial transactions."
- **verified on / by:**
- **recheck by:** 90 days after verification
- **status:** candidate
- **version:** v1

## Candidate facts to find (work queue)

Topics the first playbooks need. None may be used until it is found in a primary source and verified. The words on a page come from the source, not from this list.

| Topic | Needed by | Where to look | Status (30 Sep 2026) |
|---|---|---|---|
| Customer liability for transactions before 1 January 2027: reporting windows, limits, the 10 working day credit, the 90 day settlement | F2 | RBI (Commercial Banks - Responsible Business Conduct) Directions, 2025, paragraphs 64 to 76 (https://rbidocs.rbi.org.in/rdocs/notification/PDFs/170MD.PDF). The 2017 circular is withdrawn; RBI moved its text into these Directions "as-is". | Blocked: the PDF host shows a CAPTCHA to scripts. Satya downloads it (STATE.md, user to-do). Draft blocks from the 2017 text are kept in `.cache/research/c/` for re-quoting. |
| The same rules for regional rural banks, small finance banks, payments banks and co-operative banks, before and after 1 January 2027 | F2 (Odisha readers often bank with a regional rural bank) | RBI Third Amendment Directions of 24 June 2026 for each bank type (NotificationUser Ids 13544 to 13549), and their 2025 Directions | Not started |
| When a customer can go to the RBI Ombudsman | F1, F2 | RB-IOS 2026 | Drafted: RBI-OMB-01 to 10 |
| Report to 1930 and cybercrime.gov.in quickly so money can be frozen | F1, F2 | I4C or Home Ministry page, cybercrime.gov.in | Drafted: I4C-REPORT-01 and 02. No national time window found. A Delhi-only, undated portal PDF gives a 24-hour rule; not used. |
| The I4C Money Restoration Module: who can apply, and how | F1, F2 | Money Restoration Portal (mrm-ncrp.mha.gov.in) | Drafted: I4C-MRM-01 to 10. The SOP of 2 January 2026 that the FAQ refers to is not published. |
| A police station must register an FIR even if the crime happened elsewhere (Zero FIR) | F1 to F5, E7 | BNSS 2023, section 173 | Drafted: BNSS-ZEROFIR-01 to 06, from the Gazette. Still to do: India Code copy (amendments), whether cyber fraud is cognizable (Bharatiya Nyaya Sanhita, First Schedule), section 173(3) preliminary enquiry. |
| e-Zero FIR for large cyber fraud losses | F1, F2 | MHA release of 19 May 2025 (PIB 2129715): Delhi pilot, losses above ₹10 lakh | Found, not drafted: Delhi only, and no later official text on a wider rollout. |
| What the sideloaded adult apps do, per the advisory | seed card 1 | I4C advisory PDF (https://i4c.mha.gov.in/theme/resources/advisories/ADVISORY-TAU-ADV-NIGHTPLAY-INSTAGRAM-ADS.pdf) | Drafted from CyberDost only: I4C-ADV-2026-08-01 to 03. The PDF was not reachable (K9). |
| Ombudsman compensation limits, awards and appeals | F1, F2 (later) | RB-IOS 2026, clauses 8(3), 15 and 17 | Found, not drafted (research notes in `.cache/research/c/`) |
| Credit bureaus must alert you when your credit report is accessed | F4 | RBI circular to credit information companies (2023) | Not started |
| Compensation when a credit complaint is not settled in time | F4 | the same RBI framework | Not started |
| SMS is blocked for a period after a SIM replacement | F3, F4 | DoT order | Not started |
| How far back you can see your Aadhaar authentication history | F4 | uidai.gov.in | Not started |
| What the Aadhaar biometric lock blocks, and how to unlock it for a short time | F4 | uidai.gov.in | Not started |
| No police officer or agency arrests anyone on a video call | F5 | I4C advisory on "digital arrest" | Not started |
