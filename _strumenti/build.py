#!/usr/bin/env python3
"""Genera le pagine del sito no pAIn™.

Sorgenti: _strumenti/pagine/*.html (solo il contenuto centrale, in italiano).
Uscita:   le pagine .html nella cartella principale del sito.

Uso:  python3 _strumenti/build.py
"""
import pathlib
import re

TOOLS = pathlib.Path(__file__).resolve().parent
OUT = TOOLS.parent
VERSION = "20260918b"

# Nomi ideati dall'autore: mai tradotti, sempre con ™
TM_TERMS = ["digital4help", "watch4help", "button4help", "no pAIn"]
TM_RE = re.compile(r"(digital4help|watch4help|button4help|no pAIn)(?!™)")

PAGES = [
    # file, voce di menu, titolo, descrizione
    ("index.html", "Progetto", "no pAIn digital4help",
     "no pAIn: la tutela digitale contro la violenza di genere. App e dispositivi che chiedono aiuto con la voce o con un gesto, senza dover parlare con nessuno."),
    ("prodotti.html", "Le app", "no pAIn — Le app",
     "Le app del progetto no pAIn: AI help You, Proteggimi, no pAIn per iPhone, AIuto SOS watch4help per Wear OS, AI help App."),
    ("button4help.html", "button4help", "button4help — no pAIn",
     "button4help, il pulsante Bluetooth che fa scattare l'allarme delle app no pAIn a distanza. Cos'è, cosa non è, dove acquistarlo."),
    ("versioni.html", "Free e Premium", "no pAIn — Free e Premium",
     "Cosa è incluso nelle versioni gratuite e Premium delle app no pAIn per Android e iPhone, con il confronto completo delle funzioni."),
    ("come-funziona.html", "Come funziona", "no pAIn — Come funziona",
     "Come si attivano le app no pAIn, quali azioni partono, come funziona watch4help e come preparare la prima configurazione."),
    ("video.html", "Video", "no pAIn — Video e demo",
     "I video del progetto no pAIn: la posizione inviata dal telefono della vittima, le demo delle app, lo smartwatch e il pulsante button4help."),
    ("tutorial.html", "Tutorial", "no pAIn — Tutorial",
     "I videotutorial del progetto no pAIn: configurazione, contatti su Telegram, abbinamento di button4help e smartwatch. Pagina in costruzione."),
    ("ricerca.html", "Ricerca", "no pAIn — Tecnologia e ricerca",
     "La tecnologia e le pubblicazioni scientifiche del progetto no pAIn del Prof. Ing. Agostino Giorgio, Politecnico di Bari."),
    ("collabora-con-noi.html", "Collabora", "no pAIn — Collabora con noi",
     "Collabora con il progetto no pAIn del Politecnico di Bari: cerchiamo artigiani e aziende orafe per nascondere button4help in gioielli e accessori indossabili."),
    ("collabora.html", "Enti e aziende", "no pAIn — Collabora",
     "Porta no pAIn nella tua organizzazione: enti pubblici, associazioni, aziende e sponsor.", False),
    ("domande.html", "Domande", "no pAIn — Domande frequenti",
     "Risposte chiare sulle app no pAIn, su button4help, sulla connessione, sulla privacy e sui costi.", False),
]

LANG_OPTIONS = [
    ("it", "Italiano"), ("en", "English"), ("fr", "Français"), ("de", "Deutsch"),
    ("es", "Español"), ("tr", "Türkçe"), ("el", "Ελληνικά"), ("pt", "Português"),
    ("ro", "Română"), ("pl", "Polski"), ("nl", "Nederlands"), ("sv", "Svenska"),
]

HEAD = """<!doctype html>
<html lang="it" data-lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>
/* sceglie la lingua prima di mostrare la pagina: ?lang= → scelta salvata → lingua del browser → italiano */
(function () {{
  var L = ['it','en','fr','de','es','tr','el','pt','ro','pl','nl','sv'], l = null, d = document.documentElement;
  try {{ l = new URLSearchParams(location.search).get('lang'); }} catch (e) {{}}
  if (L.indexOf(l) < 0) {{ try {{ l = localStorage.getItem('np-lang'); }} catch (e) {{}} }}
  if (L.indexOf(l) < 0) {{
    l = null;
    var n = navigator.languages || [navigator.language || ''];
    for (var i = 0; i < n.length && !l; i++) {{ var c = String(n[i]).slice(0, 2).toLowerCase(); if (L.indexOf(c) >= 0) l = c; }}
  }}
  l = l || 'it';
  d.setAttribute('data-lang', l);
  if (l !== 'it') {{ d.classList.add('np-wait'); setTimeout(function () {{ d.classList.remove('np-wait'); }}, 2500); }}
}})();
</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/no-pain-app-family.jpg">
<meta name="theme-color" content="#000a49">
<link rel="icon" href="assets/favicon-64.png" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&amp;family=Familjen+Grotesk:wght@500;600;700&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap">
<link rel="stylesheet" href="style.css?v={version}">
</head>
<body>

<header class="site-header">
  <div class="wrap">
    <a class="logo" href="index.html" data-no-i18n><span class="shield"><img src="assets/logo-scudo.png" alt="" width="84" height="84"></span><span class="word">no p<b>AI</b>n<span class="tm">™</span></span></a>
    <nav class="nav" id="menu" aria-label="Navigazione principale">
{nav}
      <a class="nav-cta" href="#contatti">Contatti</a>
    </nav>
    <div class="header-tools">
      <div class="lang-switch" data-no-i18n>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>
        <span class="lang-code" aria-hidden="true">IT</span>
        <select id="lang-select" aria-label="Lingua · Language">
{options}
        </select>
      </div>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu" data-no-i18n>Menu</button>
    </div>
  </div>
</header>

<main id="main">
"""

FOOT = """
</main>

<section class="contact-band" id="contatti">
  <div class="wrap">
    <div>
      <span class="eyebrow">Prezzi, disponibilità e collaborazioni</span>
      <h2 style="margin-top:16px">Troviamo la soluzione adatta a te.</h2>
      <address>
        <strong>Prof. Ing. Agostino Giorgio</strong>
        <span>Dipartimento di Ingegneria Elettrica e dell'Informazione</span>
        <span>Politecnico di Bari · Via Re David, 200 · 70125 Bari</span>
        <a href="tel:+390805963239">Tel. ufficio: 080 596 3239/579</a>
        <a href="mailto:agostino.giorgio@poliba.it" data-no-i18n>agostino.giorgio@poliba.it</a>
        <a href="https://www.instagram.com/no_pain_app/" target="_blank" rel="noopener" data-no-i18n>Instagram: @no_pain_app ↗</a>
      </address>
    </div>
    <div class="contact-options">
      <a class="contact-option" href="mailto:agostino.giorgio@poliba.it" data-mail="private"><span><strong>Informazioni per privati</strong><span>App, button4help e compatibilità con il tuo telefono</span></span><span class="arr">↗</span></a>
      <a class="contact-option" href="mailto:agostino.giorgio@poliba.it" data-mail="partner"><span><strong>Proposte per enti e aziende</strong><span>Dimostrazioni e collaborazioni</span></span><span class="arr">↗</span></a>
      <p class="small">Si aprirà la tua app di posta. Puoi scrivere anche direttamente a <a href="mailto:agostino.giorgio@poliba.it">agostino.giorgio@poliba.it</a></p>
    </div>
  </div>
</section>

<footer class="site-footer">
  <div class="wrap">
    <div>
      <a class="logo" href="index.html" data-no-i18n><span class="shield"><img src="assets/logo-scudo.png" alt="" width="84" height="84"></span><span class="word">no p<b>AI</b>n<span class="tm">™</span></span></a>
      <p style="margin-top:12px">Progetto del Prof. Ing. Agostino Giorgio<br>Docente del Politecnico di Bari</p>
      <p class="visits" hidden><span class="visits-label">Visite al sito</span> <b id="visit-count" data-no-i18n></b></p>
    </div>
    <div>
      <h4>Il sito</h4>
      <ul>
{footnav}
      </ul>
    </div>
    <div>
      <h4>Risorse</h4>
      <ul>
        <li><a href="https://poliba.wixsite.com/no_pain_privacy" target="_blank" rel="noopener">Manuali e privacy delle app ↗</a></li>
        <li><a href="assets/guida-no-pain-android.pdf" target="_blank" rel="noopener">Manuale Proteggimi per Android (PDF) ↗</a></li>
        <li><a href="assets/no-pain-presentazione.pdf" target="_blank" rel="noopener">Presentazione del progetto (PDF, in italiano) ↗</a></li>
        <li><a href="https://www.instagram.com/no_pain_app/" target="_blank" rel="noopener">Instagram ↗</a></li>
      </ul>
    </div>
    <p class="fineprint"><span>In caso di pericolo immediato chiama il 112. Le app no pAIn avvisano i contatti di emergenza scelti da te e non sostituiscono i servizi pubblici di emergenza.</span> <span data-no-i18n>© <span id="year">2026</span> no pAIn</span> · <span>Informati. Configura. Prova.</span></p>
  </div>
</footer>

<script src="site.js?v={version}"></script>
</body>
</html>
"""


def add_tm(html: str) -> str:
    """Aggiunge ™ ai nomi solo nel testo visibile e negli attributi descrittivi, mai in link o nomi di file."""
    parts = re.split(r"(<[^>]+>)", html)
    in_skip = False
    for i, part in enumerate(parts):
        if part.startswith("<"):
            low = part.lower()
            if low.startswith(("<script", "<style")):
                in_skip = True
            elif low.startswith(("</script", "</style")):
                in_skip = False
            continue
        if not in_skip:
            parts[i] = TM_RE.sub(r"\1™", part)
    html = "".join(parts)
    # nomi spezzati dall'evidenziazione colorata
    html = re.sub(r'button<span class="hl">4help</span>(?!™)', 'button<span class="hl">4help</span>™', html)
    return html


def main():
    options = "\n".join(f'          <option value="{c}">{n}</option>' for c, n in LANG_OPTIONS)
    pages = [(p + (True,))[:5] for p in PAGES]
    footnav = "\n".join(f'        <li><a href="{f}">{add_tm(l)}</a></li>' for f, l, _, _, _ in pages)
    for file, _, title, desc, _ in pages:
        nav = "\n".join(
            f'      <a href="{f}"{" aria-current=" + chr(34) + "page" + chr(34) if f == file else ""}>{add_tm(l)}</a>'
            for f, l, _, _, in_nav in pages if in_nav or f == file)
        body = (TOOLS / "pagine" / file).read_text()
        html = (HEAD.format(title=add_tm(title), desc=add_tm(desc), nav=nav, options=options, version=VERSION)
                + add_tm(body)
                + add_tm(FOOT.format(footnav=footnav, version=VERSION)))
        html = add_tm(html)  # idempotente: non raddoppia il simbolo
        assert "™™" not in html, file
        (OUT / file).write_text(html)
        print("scritto", file, len(html))


if __name__ == "__main__":
    main()
