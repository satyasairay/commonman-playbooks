"""Check every quote in rules/facts.md and rules/contacts.md against its snapshot.

Run from the repo root:  python .cache/tools/check_quotes.py

For each source row in the facts.md "Sources" table: the raw file
.cache/sources/<id>.<ext> must exist and its SHA-256 must match the table.
For each fact block and each contact row with a source id and a quote:
the quote must appear in .cache/sources/<id>.txt.
  EXACT      the quote appears as written
  WS-ONLY    it appears only after collapsing whitespace (line breaks in PDFs)
  MISSING    it does not appear
For each contact: the quote must show the value, or (for a URL that is the
source page itself) the value must equal the source's URL.
Exit code 1 if any snapshot is missing, any hash differs, any quote is
MISSING, or any contact value is not shown.
Files may use LF or CRLF line endings.
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / ".cache" / "sources"
FACTS = ROOT / "rules" / "facts.md"
CONTACTS = ROOT / "rules" / "contacts.md"

WS = re.compile(r"\s+")
CRLF = "\r\n"


def load(path):
    return path.read_text(encoding="utf-8").replace(CRLF, "\n")


def norm(s):
    return WS.sub(" ", s).strip()


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def unquote(q):
    q = q.strip()
    if len(q) >= 2 and q[0] in "\"“" and q[-1] in "\"”":
        q = q[1:-1]
    return q.replace("\\|", "|")


def read_sources():
    text = load(FACTS)
    sec = text.split("## Sources", 1)[1].split("\n## ", 1)[0]
    rows = {}
    for line in sec.splitlines():
        if not line.startswith("| src-"):
            continue
        c = cells(line)
        rows[c[0]] = {"url": c[3], "sha": c[4].strip("`")}
    return rows


def read_facts():
    text = load(FACTS)
    body = text.split("\n## Facts", 1)[1]
    body = body.split("\n## Candidate facts", 1)[0]
    out = []
    for block in re.split(r"\n### ", body)[1:]:
        fid = block.split("\n", 1)[0].strip()
        src = re.search(r"- \*\*source:\*\* (src-[a-z0-9-]+)", block)
        quo = re.search(r"- \*\*quote:\*\* (.+)", block)
        out.append((fid, src.group(1) if src else None,
                    unquote(quo.group(1)) if quo else None))
    return out


def read_contacts():
    out = []
    for line in load(CONTACTS).splitlines():
        if not re.match(r"\| C\d\d ", line):
            continue
        c = cells(line)
        src = re.search(r"src-[a-z0-9-]+", c[5])
        out.append((c[0], src.group(0) if src else None,
                    unquote(c[6]) if c[6] else None, c[2], c[3]))
    return out


def host(url):
    return re.sub(r"^https?://", "", url).split("/")[0].lower()


def check_values(contacts, sources):
    """A contact's quote must state its value, or (for a URL that is the
    source page itself) the value must equal the source's URL."""
    bad = 0
    print("\n## Contact values")
    for iid, sid, quote, value, ctype in contacts:
        if not sid or not quote:
            continue
        q = norm(quote).lower()
        if ctype.startswith("url"):
            h = host(value)
            if h in q or h.replace("www.", "") in q.replace("www.", ""):
                verdict = "VALUE IN QUOTE"
            elif sid in sources and value == sources[sid]["url"]:
                verdict = "PAGE ITSELF"
            else:
                verdict = "VALUE NOT SHOWN"
                bad += 1
        else:
            verdict = "VALUE IN QUOTE" if value.lower() in q else "VALUE NOT SHOWN"
            bad += verdict == "VALUE NOT SHOWN"
        print(f"contact {iid}: {verdict}")
    return bad


def main():
    bad = 0
    sources = read_sources()
    texts = {}
    print("## Snapshots")
    for sid, row in sources.items():
        raws = [p for p in SRC_DIR.glob(sid + ".*") if p.suffix != ".txt"]
        txt = SRC_DIR / (sid + ".txt")
        if not raws or not txt.exists():
            print(f"{sid}: SNAPSHOT MISSING")
            bad += 1
            continue
        sha = hashlib.sha256(raws[0].read_bytes()).hexdigest()
        ok = sha == row["sha"]
        bad += 0 if ok else 1
        print(f"{sid}: {raws[0].name} sha {'OK' if ok else 'DIFFERS ' + sha}")
        texts[sid] = txt.read_text(encoding="utf-8")
    print("\n## Quotes")
    contacts = read_contacts()
    for kind, items in (("fact", read_facts()),
                        ("contact", [c[:3] for c in contacts])):
        for iid, sid, quote in items:
            if not sid or not quote:
                print(f"{kind} {iid}: no source or no quote (skipped)")
                continue
            if sid not in texts:
                print(f"{kind} {iid}: {sid} not in sources table or no snapshot")
                bad += 1
                continue
            t = texts[sid]
            if quote in t:
                verdict = "EXACT"
            elif norm(quote) in norm(t):
                verdict = "WS-ONLY"
            else:
                verdict = "MISSING"
                bad += 1
            print(f"{kind} {iid}: {sid} {verdict}")
    bad += check_values(contacts, sources)
    print(f"\nproblems: {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
