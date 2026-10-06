# Contacts registry

The only place where phone numbers, WhatsApp numbers, URLs and emails for the site come from. Pages use them only through the `contact` shortcode with the contact id (rules/facts.md explains references). G1 fails the build if a page or any format contains a value that is not a reference to a `verified` row. Links to the site's own pages are exempt.

Changes to this file are NOVEL: Satya approves each one.

## Rules

- **Source:** a page on the owner's own domain (for example gov.in, nic.in, rbi.org.in, uidai.gov.in) that states the value. News stories, blogs and search snippets are not sources. The Source column holds a source id from the Sources table in rules/facts.md. The saved copy is in `.cache/sources/<source id>`.
- **Quote:** the exact words on that page that state the value.
- **A URL that is the source page itself:** a page rarely states its own address. For such a row, the quote shows what the page is for, and the value must be exactly the source's URL in the Sources table of rules/facts.md (C09, C15, C16, C17).
- **Verified:** Satya opened the source himself, saw the quote, and set the status, date and initials.
- **Re-check:** every 180 days, or when the drift monitor (L15) flags the source.
- **Never listed:** bank phone numbers. Pages tell readers to use the number on the back of their card or in their bank's official app.
- **Statuses:** `pending` (not checked), `needs-official-source` (only news supports it), `verified`, `rejected`.

## Registry

Nothing is verified yet. On 30 Sep 2026 (L02), Claude found the source and quote for each row that has a source id. Those rows wait for Satya's check. C19 to C21 are new rows found during that research.

| Id | Name | Value | Type | Owner | Source | Quote | Verified on | By | Status |
|---|---|---|---|---|---|---|---|---|---|
| C01 | National Cybercrime Helpline | 1930 | phone | I4C, Ministry of Home Affairs | src-cybercrime-01 | "Report online financial fraud at the National cybercrime helpline number 1930." | | | pending |
| C02 | National Cyber Crime Reporting Portal | https://cybercrime.gov.in | url | I4C, Ministry of Home Affairs | src-mha-01 | "The ‘National Cyber Crime Reporting Portal’ (NCRP) (https://cybercrime.gov.in) has been launched, as a part of the I4C, to enable public to report incidents pertaining to all types of cyber crimes" | | | pending |
| C03 | I4C website | https://i4c.mha.gov.in | url | I4C | none yet: the site did not answer on 30 Sep 2026 (known issue K9) | | | | pending |
| C04 | Money Restoration Portal (I4C) | https://mrm-ncrp.mha.gov.in | url | I4C, Ministry of Home Affairs | src-mrm-01 | "The victim logs in to the Money Restoration Portal (MRM) https://mrm-ncrp.mha.gov.in" | | | pending |
| C05 | RBI Complaint Management System (complaints to the RBI Ombudsman, Integrated Ombudsman Scheme, 2026) | https://cms.rbi.org.in | url | RBI | src-rbi-01 | "9. What is the procedure for filing a complaint before the RBI Ombudsman? • Online: through the CMS portal at https://cms.rbi.org.in." | | | pending |
| C06 | UIDAI helpline | 1947 | phone | UIDAI | src-uidai-01 | "Individuals can contact UIDAI Toll Free Number (1947) for concerns related to Aadhaar." | | | pending |
| C07 | UIDAI help email | help@uidai.gov.in | email | UIDAI | src-uidai-01 | "Email – Individuals can send email to help@uidai.gov.in for any queries and complaint related to Aadhaar." | | | pending |
| C08 | myAadhaar portal (UIDAI's login portal for Aadhaar services) | https://myaadhaar.uidai.gov.in/ | url | UIDAI | src-uidai-02 | "MyAadhaar portal is a login based portal containing an array of Aadhaar related services. An Aadhaar Number holder may visit MyAadhaar by clicking on https://myaadhaar.uidai.gov.in/" | | | pending |
| C09 | Sanchar Saathi (SIMs in your name, lost phone block) | https://sancharsaathi.gov.in | url | Department of Telecommunications | src-sancharsaathi-01 | "Visit Sanchar Saathi portal at www.sancharsaathi.gov.in" | | | pending |
| C10 | National Consumer Helpline | 1915 | phone | Department of Consumer Affairs | src-nch-01 | "grievance by either calling the toll free number 1800-11-4000 or 1915" | | | pending |
| C11 | NALSA legal aid helpline | 15100 | phone | National Legal Services Authority | src-nalsa-01 | "NALSA Helpline Number 15100" | | | pending |
| C12 | Nyaya Setu (Tele-Law) on WhatsApp | 7217711814 | whatsapp | Ministry of Law and Justice | none: not on tele-law.in, doj.gov.in, nyayasetu.doj.gov.in or PIB on 30 Sep 2026; news only (known issue K1) | | | | needs-official-source |
| C13 | CPGRAMS (grievances against government offices) | https://pgportal.gov.in | url | DARPG | src-pgportal-01 | "The above nodal agencies receive grievances online through pgportal.gov.in as well as by post or by hand in person, from the public." | | | pending |
| C14 | TransUnion CIBIL: raise a credit report dispute | https://www.cibil.com/consumer-dispute-resolution | url | TransUnion CIBIL | none saved: cibil.com blocks automated fetches (Cloudflare, HTTP 403). Quote seen in a browser on 30 Sep 2026; Satya checks it in his browser. | "Sign Up if you are a new user. If you are an existing user, Login to check your latest CIBIL Score & Report or raise a dispute to report any inaccuracy." | | | pending |
| C15 | Experian India: raise a credit report dispute | https://www.experian.in/consumer/consumer-services/ | url | Experian Credit Information Company of India | src-experian-01 | "Portal – Click here to raise a dispute on your credit report" | | | pending |
| C16 | Equifax India: raise a credit report dispute | https://www.equifax.co.in/support/consumer-grievance-redressal/ | url | Equifax Credit Information Services | src-equifax-01 | "Follow the below steps to raise the dispute" | | | pending |
| C17 | CRIF: raise a credit report dispute | https://www.crifhighmark.com/raise-a-dispute | url | CRIF Credit Information Services (formerly CRIF High Mark) | src-crif-01 | "Select the credit report on which dispute to be raised and click “Proceed”" | | | pending |
| C18 | WhatsApp share link (opens WhatsApp with the page's text filled in; the site learns nothing) | https://wa.me/?text= | url-base | WhatsApp (Meta) | src-whatsapp-01 | "To create a link with just a pre-filled message, use https://wa.me/?text=urlencodedtext" | | | pending |
| C19 | Tele-Law helpline (free legal advice) | 14454 | phone | Ministry of Law and Justice | src-pib-01 | "The Tele-Law programme provides free pre-litigation legal advice to citizens through video and telephonic consultations at Common Service Centres (CSCs), the Tele-Law Mobile Application and the dedicated toll-free helpline number 14454." | | | pending |
| C20 | RBI Ombudsman complaints by email | crpc@rbi.org.in | email | RBI | src-rbi-01 | "• E-mail: by sending the complaint to crpc@rbi.org.in." | | | pending |
| C21 | RBI Contact Centre (help with the Ombudsman Scheme) | 14448 | phone | RBI | src-rbi-02 | "The Contact Center with Interactive Voice Response System (IVRS) with Toll Free #14448 is available 24x7 for Complainants to know about the Scheme and the process of complaint lodging." | | | pending |

## Notes from the L02 research (30 Sep 2026)

- **C04:** the portal is on a subdomain of mha.gov.in. MHA press releases name the Money Restoration Module but do not give its address, and cybercrime.gov.in does not link to it; only the portal's own FAQ states the address. Fake "money recovery" sites are a known scam, so Satya should confirm this address himself. The portal builds its text with JavaScript; the saved copy is rendered. This closes known issue K3 once verified.
- **C08:** in a browser, myaadhaar.uidai.gov.in moves on to `myaadhaarbeta.uidai.gov.in` (page JavaScript). No UIDAI page states in its text that the authentication history is on the portal; UIDAI pages say the Aadhaar app can show it. F4 (L11) must settle this before it uses C08 for that step.
- **C10:** the same page also lists 1800-11-4000. Hours on the contact page: 8 AM to 8 PM, daily except national holidays.
- **C11:** NALSA's menu links the helpline to `nalsa15100.in`, which is not a government domain. Do not list that link unless it is checked on its own.
- **C12:** the same service has an official toll-free number, now C19. The name "Nyaya Setu" is also used for other government services, which can confuse readers.
- **C13:** the portal says grievances sent by email are not attended to, and that the government charges no fee to file one.
- **C15 to C17:** the bureaus' own pages still cite the 2021 Ombudsman Scheme, which RBI repealed on 1 July 2026. For C17, two CRIF deep links lead to a free-report sign-up form and to paid plans. Link only the raise-a-dispute page.
- **Credit bureau cross-check:** RBI lists all four credit information companies at https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=4921 (as on 18 August 2026), with email addresses but no websites.
- **C18:** the help page builds its text with JavaScript. The saved copy is the page as a browser renders it.
