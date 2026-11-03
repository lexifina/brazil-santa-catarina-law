"""Independent letters-and-digits check of every Santa Catarina law version against its source page, read with a
second reader (Python's html.parser event stream, none of the builder's code or regexes).

    python -X utf8 check_laws.py part.json ...

The page's character data inside <body>, leaving out everything inside the header block (the element with class
"procedencia") and everything from the signature block (class "assinatura") on, reduced to letters and digits, must
equal the version's unit files reduced the same way, each unit found at its place in document order. Struck text
(<s>, <strike>, <del>) counts only when it is nothing but an ordinal sign (ALESC strikes "º" as styling); a
parenthesis that opens with an alteration-note word ("Redação dada ...", "Revogado ...", "Acrescido ...") is the
publisher's note and does not count.
"""
import hashlib, json, re, sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / '.cache' / 'ia'
VOID = {'br', 'img', 'hr', 'meta', 'link', 'input', 'col', 'area', 'base', 'wbr'}


class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.body, self.done, self.skip, self.struck = [], False, False, 0, []

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.body = True
        if tag in VOID:
            return
        cls = ' '.join(v or '' for k, v in attrs if k == 'class').split()
        if 'assinatura' in cls:
            self.done = True
        if self.skip or 'procedencia' in cls or tag in ('script', 'style'):
            self.skip += 1
        if tag in ('s', 'strike', 'del'):
            self.struck.append([])

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.skip:
            self.skip -= 1
        if tag in ('s', 'strike', 'del') and self.struck:
            inner = ''.join(self.struck.pop())
            if set(inner) <= set('ºª°oa \xa0\t\r\n'):
                self.emit(inner)

    def handle_data(self, data):
        if self.struck:
            self.struck[-1].append(data)
        else:
            self.emit(data)

    def emit(self, data):
        if self.struck:
            self.struck[-1].append(data)
        elif self.body and not self.done and not self.skip:
            self.out.append(data)


def ld(s):
    return ''.join(ch for ch in s if ch.isalnum())


def source_text(raw):
    s = raw.decode('utf-8', 'replace')
    if '�' in s:
        s = raw.decode('cp1252', 'replace')
    r = Reader()
    r.feed(s)
    t = ' '.join(r.out)
    return re.sub(r'\(\s*(?:Reda[çc][ãa]o|Acrescentad|Acrescid|Revogad|Inclu[íi]d|Suprimid|Renumerad|Alterad|Vide\s|'
                  r'Vetad|Declarad|Suspens|Ver\s)[^()]*\)', ' ', t, flags=re.I)


def main(paths):
    bad = total = 0
    for p in paths:
        for a in json.load(open(p, encoding='utf-8'))['acts']:
            for v in a['versions']:
                path = RAW / hashlib.sha256(v['source_url'].encode()).hexdigest()
                raw = path.read_bytes()
                assert hashlib.sha256(raw).hexdigest() == v['sha256'], (a['slug'], 'sha256')
                total += 1
                src = ld(source_text(raw))
                rest = {k: ld(re.sub(r'(?m)^#+ ', '', u['text'])) for k, u in v['units'].items()}
                pos = 0
                while rest:
                    hit = None
                    for k, t in rest.items():
                        if t and src.startswith(t, pos) and (hit is None or len(t) > len(rest[hit])):
                            hit = k
                    if hit is None:
                        break
                    pos += len(rest.pop(hit))
                if rest or pos != len(src):
                    bad += 1
                    print(f'MISMATCH {a["slug"]} {v["from"]}: matched {pos}/{len(src)}; next source: '
                          f'{src[pos:pos + 80]!r}; unplaced: {list(rest)[:5]}')
    print(f'{total} versions checked, {bad} mismatches')
    return bad


if __name__ == '__main__':
    sys.exit(1 if main(sys.argv[1:]) else 0)
