#!/usr/bin/env python3
"""Converte le traduzioni nei file lang/xx.js e le controlla.

Ingresso:
  _strumenti/traduzioni/it.json      testi italiani raccolti dal sito (codice → testo)
  <cartella>/xx.txt                  righe "NNN|testo tradotto" (NNN = numero in it.json)
                                     più righe "ui.menu|…", "mail.privateSubject|…" (\\n = a capo)
Uscita:
  lang/xx.js                         caricato dal sito quando si sceglie la lingua
  _strumenti/traduzioni/xx.json      archivio: codice → {it, tr}, riusabile quando cambiano i testi

Uso:  python3 _strumenti/traduzioni.py CARTELLA_TXT en fr de ...
"""
import json
import pathlib
import re
import sys
from collections import Counter

TOOLS = pathlib.Path(__file__).resolve().parent
SITE = TOOLS.parent
ARCH = TOOLS / "traduzioni"

TAG = re.compile(r"<[^>]+>")
NUM = re.compile(r"\d+")


def check(it, tr):
    problems = []
    if Counter(TAG.findall(it)) != Counter(TAG.findall(tr)):
        problems.append("tag/link diversi")
    if it.count("™") != tr.count("™"):
        problems.append(f"™ {it.count('™')}→{tr.count('™')}")
    if Counter(NUM.findall(it)) != Counter(NUM.findall(tr)):
        problems.append(f"numeri {sorted(NUM.findall(it))}→{sorted(NUM.findall(tr))}")
    return problems


def main():
    src_dir = pathlib.Path(sys.argv[1])
    langs = sys.argv[2:]
    items = json.loads((ARCH / "it.json").read_text())  # [{"n": "001", "k": ..., "it": ...}]
    by_n = {e["n"]: e for e in items}
    (SITE / "lang").mkdir(exist_ok=True)
    for lang in langs:
        t, ui, mail, report = {}, {}, {}, []
        for line in (src_dir / f"{lang}.txt").read_text().splitlines():
            if not line.strip() or "|" not in line:
                continue
            n, text = line.split("|", 1)
            n, text = n.strip(), text.strip()
            if n.startswith("ui."):
                ui[n[3:]] = text
                continue
            if n.startswith("mail."):
                mail[n[5:]] = text.replace("\\n", "\n")
                continue
            e = by_n.get(n)
            if not e:
                report.append(f"  {n}: numero inesistente")
                continue
            p = check(e["it"], text)
            if p:
                report.append(f"  {n}: {', '.join(p)}\n     IT: {e['it'][:140]}\n     {lang.upper()}: {text[:140]}")
            t[e["k"]] = text
        missing = [e["n"] for e in items if e["k"] not in t]
        data = {"ui": ui, "mail": mail, "t": t}
        js = ("// no pAIn™ — traduzione " + lang + " (generata da _strumenti/traduzioni.py)\n"
              "(window.NP_LANGS = window.NP_LANGS || {})." + lang + " = "
              + json.dumps(data, ensure_ascii=False, indent=0) + ";\n")
        (SITE / "lang" / f"{lang}.js").write_text(js)
        archive = {e["k"]: {"it": e["it"], "tr": t[e["k"]]} for e in items if e["k"] in t}
        archive["_ui"], archive["_mail"] = ui, mail
        (ARCH / f"{lang}.json").write_text(json.dumps(archive, ensure_ascii=False, indent=1))
        print(f"{lang}: {len(t)} testi tradotti, {len(missing)} lasciati uguali all'italiano, "
              f"ui {len(ui)}/3, mail {len(mail)}/4, {len(report)} da controllare")
        if missing:
            print("  uguali all'italiano:", " ".join(missing))
        for r in report:
            print(r)


if __name__ == "__main__":
    main()
