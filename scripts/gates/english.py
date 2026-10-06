"""British English membership using the committed Hunspell data, stdlib only.

This is a conservative word-list expansion, not a full Hunspell engine.
Single affixes and permitted prefix/suffix crosses are expanded. Unrecognised
compounds fail closed rather than being guessed from component words.
"""
import functools
import re
from pathlib import Path

DICT = Path(__file__).resolve().parent / 'dictionary'


def apply(word, rule):
    kind, strip, add, condition = rule
    pattern = '^' + condition if kind == 'PFX' else condition + '$'
    if not re.search(pattern, word):
        return None
    strip = '' if strip == '0' else strip
    add = '' if add == '0' else add.split('/')[0]
    if kind == 'PFX':
        return add + word[len(strip):] if word.startswith(strip) else None
    if strip and not word.endswith(strip):
        return None
    return (word[:-len(strip)] if strip else word) + add


@functools.lru_cache(maxsize=1)
def words():
    rules, crosses = {}, set()
    for line in (DICT / 'en_GB.aff').read_text(encoding='utf-8-sig').splitlines():
        cells = line.split()
        if len(cells) == 4 and cells[0] in {'PFX', 'SFX'}:
            if cells[2] == 'Y':
                crosses.add((cells[0], cells[1]))
        elif len(cells) >= 5 and cells[0] in {'PFX', 'SFX'}:
            rules.setdefault(cells[1], []).append((cells[0], cells[2], cells[3], cells[4]))
    out = set()
    for line in (DICT / 'en_GB.dic').read_text(encoding='utf-8-sig').splitlines()[1:]:
        token = line.split()[0]
        word, _, flags = token.partition('/')
        out.add(word.lower())
        prefixes, suffixes = [], []
        for flag in flags:
            for rule in rules.get(flag, []):
                formed = apply(word, rule)
                if formed:
                    out.add(formed.lower())
                    if (rule[0], flag) in crosses:
                        (prefixes if rule[0] == 'PFX' else suffixes).append(rule)
        for prefix in prefixes:
            for suffix in suffixes:
                formed = apply(apply(word, prefix), suffix)
                if formed:
                    out.add(formed.lower())
    return out


def allowed(path):
    out = set()
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) == 4 and cells[3].startswith('approved'):
            out.update(w.lower() for w in re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", cells[0]))
            out.update(w.lower() for w in re.findall(r'[A-Za-z]+', cells[0]))
    return out


def errors(text, allowed_words):
    errors = []
    if re.search(r'[\u0900-\u097f\u0b00-\u0b7f]', text):
        errors.append('non-English script')
    dictionary = words() | allowed_words
    for word in re.findall(r"[^\W\d_]+(?:['’][^\W\d_]+)*", text, re.UNICODE):
        normal = word.lower().replace('’', "'")
        # Common Hinglish must fail even when a dictionary includes it as a name.
        if normal in {'paisa', 'karein', 'jaldi', 'ji'} or normal not in dictionary:
            errors.append(f'word outside en_GB and allowed terms: {word}')
    for sentence in re.split(r'[.!?]+(?:\s|$)|\n+', text):
        count = len(re.findall(r"[^\W\d_]+(?:['’][^\W\d_]+)*", sentence))
        if count > 25:
            errors.append(f'sentence has {count} words (limit 25)')
    return errors
