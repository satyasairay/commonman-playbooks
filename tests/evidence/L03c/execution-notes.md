# Execution blocks and their causes

No implementation step remains blocked. All three branches were pushed and their stacked PRs opened. These notes retain the causes encountered during execution rather than treating transient environment failures as failed controls.

- Git initially rejected the clone as owned by another Windows SID. A per-command safe.directory setting resolved the read check; no global trust or Git identity was changed. The sandbox makes .git read-only, so authorized commits/pushes used reviewed escalation.
- Hugo's WinGet symlink could not execute in the restricted shell. The installed executable was copied into ignored .cache/bin and used for local builds. CI verifies the pinned release checksum independently.
- Python was absent from PATH. Local checks use the already installed runtime's absolute path; no Python installation was required.
- The restricted shell could not use gh's stored token. Existing authentication worked for approved commands outside the sandbox. No alternate login, token creation or account change was attempted.
- The browser inventory was empty, the in-app browser unavailable and no local browser installed. The existing CI Chrome provides actual screenshots, native interaction and page network evidence.
- Local Poppler has pdfinfo and pdftoppm but no pdftotext. Actual PDF generation and text checks run in CI with poppler-utils; local PDF work was read-only inspection of the downloaded artefact.
- The first L03c CI format check counted WeasyPrint's generated list label as extra PDF text. A failing test preceded the bounded normalization fix: whitespace and one expected label per step may differ; additional visible text still fails.
- The next CI run passed G12 but its global Chrome net log included unrelated clock/update/account requests. The final harness records the actual page target from before navigation, rejects empty traces or outside requests and opens details through native input. Its request-origin control is mutation-checked.
- A GNU licence-text download endpoint failed; the same licence text was retained from the official GCC mirror, alongside the dictionary's original attribution and upstream pin.
- Source hash writes to protected rules are forbidden by the card. The fetch wrapper therefore emits proposals; applying a real source hash or real verification remains Satya's work.

The remaining work belongs to the human gates: Claude review of each PR, Satya's draft wording and signature/footer decisions, real source/fact/contact verification (including C18), private vulnerability reporting, security.txt expiry approval, branch protection and Satya's merge. Deployment/headers/log checks belong to L06; no VPS or account settings were touched.
