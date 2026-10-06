"""Fetch one URL, save the raw bytes and a plain-text copy, print SHA-256.

Usage:
  python fetch_text.py <url> <out_base>          # writes <out_base>.<ext> and <out_base>.txt
  python fetch_text.py --text <file>              # re-extract text from a saved file

Text rules (same for every source, so quotes can be checked word for word):
  HTML: visible text only (script, style, noscript dropped), block tags become new lines.
  PDF:  pdftotext -layout is NOT used; plain reading order (pdftotext default).
  Whitespace inside a line is collapsed to one space; blank lines are dropped.
"""
import hashlib
import html
import re
import shutil
import ssl
import subprocess
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

BLOCK = {"p", "div", "br", "li", "tr", "td", "th", "h1", "h2", "h3", "h4",
         "h5", "h6", "section", "article", "header", "footer", "table",
         "ul", "ol", "dd", "dt", "blockquote", "pre", "option", "title"}
SKIP = {"script", "style", "noscript", "svg", "template"}


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        elif tag in BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip:
            self.skip -= 1
        elif tag in BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def tidy(text):
    lines = []
    for line in text.replace("\r", "\n").split("\n"):
        line = re.sub(r"[ \t ​]+", " ", line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines) + "\n"


def html_to_text(raw):
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            doc = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    p = TextParser()
    p.feed(doc)
    return tidy(html.unescape("".join(p.parts)))


def pdf_to_text(path):
    exe = shutil.which("pdftotext")
    if not exe:
        sys.exit("pdftotext not found")
    out = subprocess.run([exe, "-enc", "UTF-8", str(path), "-"],
                         capture_output=True, check=True)
    return tidy(out.stdout.decode("utf-8", "replace"))


def to_text(path, raw):
    if raw[:5] == b"%PDF-":
        return pdf_to_text(path)
    return html_to_text(raw)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "*/*"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
        return r.read(), r.headers.get("Content-Type", ""), r.geturl()


def main():
    if sys.argv[1] == "--text":
        path = Path(sys.argv[2])
        raw = path.read_bytes()
        txt = to_text(path, raw)
        path.with_suffix(".txt").write_text(txt, encoding="utf-8")
        print("text:", path.with_suffix(".txt"))
        return
    url, base = sys.argv[1], Path(sys.argv[2])
    base.parent.mkdir(parents=True, exist_ok=True)
    raw, ctype, final = fetch(url)
    ext = ".pdf" if raw[:5] == b"%PDF-" else ".html"
    raw_path = base.with_suffix(ext)
    raw_path.write_bytes(raw)
    txt = to_text(raw_path, raw)
    base.with_suffix(".txt").write_text(txt, encoding="utf-8")
    print("url:", url)
    print("final_url:", final)
    print("content_type:", ctype)
    print("raw:", raw_path, len(raw), "bytes")
    print("sha256:", hashlib.sha256(raw).hexdigest())
    print("text:", base.with_suffix(".txt"), len(txt), "chars")


if __name__ == "__main__":
    main()
