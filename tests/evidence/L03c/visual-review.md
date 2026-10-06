# L03c visual review

Oracle: the LOOP CARD, rules/formats.md and rules/house-rules.md require a readable 320px web page, native evidence details, no third-party loads, and a black-and-white one-page A4 sheet with text at least 12pt. This is inspection evidence for review, not publication approval.

Provenance: Actions run 37460549015, implementation head 3afea397e072663f3daab58e8ed7e514c1ca622d, tested PR merge c229e4f03dc25cb983883f6a82b4e4e86d0575fb. The PNGs were downloaded from that run and inspected at their original resolution without editing. All content is isolated TEST content.

| Surface/state | Evidence | Observation |
|---|---|---|
| Chrome 154.0.8037.57, mobile viewport 320x1400, DPR 1, details closed | web-320-closed.png | Opening and title at top; source step and TEST contact fit the width; native summary around y530; trust and correction/footer text readable below. No overlap or clipped text. |
| Same browser and viewport, details expanded through an actual native summary click | web-320-expanded.png | Source title/location, quote, conditions and TEST check date visible around y570-740. Footer remains visible within the captured viewport. No overlap or horizontal clipping. |
| WeasyPrint 66.0 A4 PDF, Poppler render at 110 dpi, 910x1287 PNG | print-1.png, print.pdf | Opening, title, unchanged first step/contact, draft status, large page address and no-contact line fit on one page with clear margins. Black text on white, no QR. The unused lower area is expected for a single TEST step. |

The programmatic layout check reports a 320px layout viewport and content width at most 321px in both browser states. The raw browser-page-network.json and browser-evidence.json record only localhost page, stylesheet and favicon requests; there are zero outside page requests. The automatic favicon probe returns 404 because no favicon is declared; there is no broken content asset visible in either capture. These page-target events exclude Chrome's unrelated background services, which caused the prior global-net-log attempt to fail.

G12 checks the print HTML's 12pt minimum, the actual PDF's one-page count and extracted visible text against the HTML. It also rejects a two-page PDF, a foreign step, overlong WhatsApp and disabled controls, with backup restoration proven green. WhatsApp is 281 Unicode characters, including its final newline; it is plain text and was checked through exact canonical parity rather than a screenshot.

No visual defect was observed in the three inspected captures. Coverage is this TEST page in the two recorded browser states and the actual single-page PDF. Real Android hardware, other browsers, Odia/Hindi, long real playbooks and physical printing were not tested by this loop. Human checks of all draft labels, claims and actual facts remain required.
