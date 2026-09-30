# Contacts registry

The only place where phone numbers, WhatsApp numbers, URLs and emails for the site come from. Pages use them only through the `contact` shortcode with the contact id (rules/facts.md explains references). G1 fails the build if a page or any format contains a value that is not a reference to a `verified` row. Links to the site's own pages are exempt.

Changes to this file are NOVEL: Satya approves each one.

## Rules

- **Source:** a page on the owner's own domain (for example gov.in, nic.in, rbi.org.in, uidai.gov.in) that states the value. News stories, blogs and search snippets are not sources.
- **Quote:** the exact words on that page that state the value.
- **Verified:** Satya opened the source himself, saw the quote, and set the status, date and initials.
- **Re-check:** every 180 days, or when the drift monitor (L15) flags the source.
- **Never listed:** bank phone numbers. Pages tell readers to use the number on the back of their card or in their bank's official app.
- **Statuses:** `pending` (not checked), `needs-official-source` (only news supports it), `verified`, `rejected`.

## Registry

Nothing is verified yet. Values below are candidates for L02.

| Id | Name | Value | Type | Owner | Source (candidate) | Quote | Verified on | By | Status |
|---|---|---|---|---|---|---|---|---|---|
| C01 | National Cybercrime Helpline | 1930 | phone | I4C, Ministry of Home Affairs | https://www.india.gov.in/services/details/report-financial-fraud-through-the-national-cyber-crime-reporting-portal (seen in search) | | | | pending |
| C02 | National Cyber Crime Reporting Portal | https://cybercrime.gov.in | url | I4C, Ministry of Home Affairs | as C01 | | | | pending |
| C03 | I4C website | https://i4c.mha.gov.in | url | I4C | https://i4c.mha.gov.in/advisories.aspx (read 29 Sep 2026) | | | | pending |
| C04 | I4C Money Restoration Module | not found yet | url | I4C | none yet (known issue K3) | | | | needs-official-source |
| C05 | RBI Complaint Management System (Integrated Ombudsman) | https://cms.rbi.org.in | url | RBI | to find on rbi.org.in | | | | pending |
| C06 | UIDAI helpline | 1947 | phone | UIDAI | to find on uidai.gov.in | | | | pending |
| C07 | UIDAI help email | help@uidai.gov.in | email | UIDAI | to find on uidai.gov.in (value from memory; check it) | | | | pending |
| C08 | myAadhaar portal (biometric lock, authentication history) | https://myaadhaar.uidai.gov.in | url | UIDAI | to find on uidai.gov.in | | | | pending |
| C09 | Sanchar Saathi (SIMs in your name, lost phone block) | https://sancharsaathi.gov.in | url | Department of Telecommunications | to find | | | | pending |
| C10 | National Consumer Helpline | 1915 | phone | Department of Consumer Affairs | to find | | | | pending |
| C11 | NALSA legal aid helpline | 15100 | phone | National Legal Services Authority | https://nalsa.gov.in (seen in search) | | | | pending |
| C12 | Nyaya Setu (Tele-Law) on WhatsApp | 7217711814 | whatsapp | Ministry of Law and Justice | news only (known issue K1) | | | | needs-official-source |
| C13 | CPGRAMS (grievances against government offices) | https://pgportal.gov.in | url | DARPG | to find | | | | pending |
| C14 | TransUnion CIBIL (credit report dispute) | https://www.cibil.com | url | credit bureau | to find | | | | pending |
| C15 | Experian India (credit report dispute) | to find | url | credit bureau | to find | | | | pending |
| C16 | Equifax India (credit report dispute) | to find | url | credit bureau | to find | | | | pending |
| C17 | CRIF High Mark (credit report dispute) | to find | url | credit bureau | to find | | | | pending |
| C18 | WhatsApp share link (opens WhatsApp with the page's text filled in; the site learns nothing) | https://wa.me/?text= | url-base | WhatsApp (Meta) | WhatsApp's own help page on share links, to find | | | | pending |
