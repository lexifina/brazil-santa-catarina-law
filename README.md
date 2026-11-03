# Santa Catarina: law history in git

The law of the State of Santa Catarina (Estado de Santa Catarina) (Brazil) as a git history: one file per Artigo, one paragraph per line, so `git blame`, `git log` and `git diff` work line by line. The text is Portuguese, the only official language.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

## What this repository holds

| Folder | Act | Versions |
| --- | --- | ---: |
| `lei-<year>-<number>/`, `lei-promulgada-...` | 500 Leis (1947-2019) | 1 each |
| `lc-<year>-<number>/`, `lc-promulgada-...` | 0 Leis Complementares | 1 each |

Every law still in force is given once: **as enacted**, credited to itself, when ALESC's page lists no later change; otherwise as **the text in force** on the page (struck earlier wordings and alteration notes left out), credited to ALESC as the oldest version available. Earlier wordings are to be added later. Laws are added in parts of 500; the Constituição, the Emendas Constitucionais and decrees are not included yet. LexML Brasil (Senado Federal), the national legal-information network, lists the same ALESC laws (urn:lex:br;santa.catarina:estadual:...) and points to these pages.

## Source

[ALESC, Legislação Estadual (leis.alesc.sc.gov.br), through Internet Archive copies](https://leis.alesc.sc.gov.br), published by the Assembleia Legislativa do Estado de Santa Catarina (ALESC). Each version names the page it was taken from and that page's sha256, in `data/versions.json`.

## Dates

A law as enacted is dated by the Diário Oficial (or Diário da Assembleia) date its ALESC page records ("DO: 18.759 de 04/01/10"), or 45 days after it when it has no vigência clause (LINDB art. 1); a text in force by the day the Internet Archive copied the page. Commits are at noon in Florianópolis.

## How it is built

Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote Lexifina's code; it wrote no legal text, and no model runs when the history is built.

ALESC's page for each law (leis.alesc.sc.gov.br/html/<year>/<number>_<year>_<type>.html) is read from the Internet Archive's raw copy (the live site times out from our machine; coverage-wave decision D2 allows archive copies of official texts in that case). The text runs from the heading through the closing line (place and date); the header block (Procedência, Natureza, DO, Fonte) and the signatures are left out. One file per Artigo; what comes before the first article is `000-titulo`. A second reader (Python's html.parser, none of the builder's code) checks every letter and digit of each version against the page.

## How it is checked

Every version is read back from git on the day it took effect (`tools/check_repo.py`) and must match the corpus; an independent letters-and-digits comparison of every version against the source page must show no difference. Results are in `REPRODUCE.md`.

## What "author" means

The author of each commit is the law that made the text, or, for a consolidated text, the publisher, with an e-mail address that cannot exist; the committer is always Lexifina.

## Limits

Not a complete history: an amended law starts at its text in force, dated by the day the Internet Archive copied ALESC's page (the page gives no day for each change), and a law ALESC does not mark as repealed is taken as in force. The archive copy may be older than ALESC's current page. The text is not the official version: only the Diário Oficial do Estado is authoritative.

## Licence

See [LICENSE](LICENSE): Brazilian law texts are not protected by copyright (Lei 9.610/1998, art. 8, IV). Fonte: ALESC, Legislação Estadual (leis.alesc.sc.gov.br), through Internet Archive copies, Assembleia Legislativa do Estado de Santa Catarina (ALESC).
