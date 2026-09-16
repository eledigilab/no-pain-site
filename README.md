# no pAIn™ — sito del progetto

Sito statico pubblicato con GitHub Pages: https://eledigilab.github.io/no-pain-site/

## Pagine

| File | Contenuto |
|---|---|
| `index.html` | Il progetto: digital4help™, perché serve, i sei modi di attivazione, le azioni, l'ecosistema |
| `prodotti.html` | Le app: AI help You, Proteggimi, no pAIn™ iOS, AIuto SOS watch4help™ (con galleria), AI help App, AIutoSOS Apple Watch |
| `button4help.html` | Il pulsante: galleria immagini e video, cos'è, cosa non è, come si usa, link d'acquisto |
| `versioni.html` | Free e Premium con la tabella di confronto completa |
| `come-funziona.html` | Modalità di attivazione, azioni, watch4help™, prima configurazione |
| `ricerca.html` | Tecnologia, pubblicazioni, presentazione PDF |
| `collabora.html` | Proposte per enti pubblici, associazioni, aziende |
| `domande.html` | Domande frequenti |
| `style.css` | Colori, caratteri e impaginazione di tutte le pagine |
| `site.js` | Lingue, menu su telefono, visore immagini |
| `lang/` | Le traduzioni nelle 11 lingue straniere (`en.js`, `fr.js`, …) |
| `assets/` | Immagini, logo (`logo-scudo.png`), icone e presentazione PDF |
| `_strumenti/` | Script per rigenerare le pagine e le traduzioni (non serve ai visitatori) |

## Lingue

Il sito è scritto in italiano ed è tradotto in inglese, francese, tedesco, spagnolo, turco, greco,
portoghese, rumeno, polacco, olandese e svedese. La lingua si sceglie dal menu con il globo in alto;
resta memorizzata e passa da una pagina all'altra. Un link si può condividere già in una lingua
aggiungendo `?lang=en` (o `fr`, `de`, …) all'indirizzo.

I nomi **no pAIn™, digital4help™, watch4help™, button4help™** non vengono mai tradotti e hanno sempre il ™.

**Se cambi una frase italiana**, nelle altre lingue quella frase resterà in italiano finché non viene
ritradotta: il sito non mostra mai una traduzione vecchia di un testo cambiato.

## Galleria immagini e video

In `prodotti.html` (sezione AIuto SOS) e in `button4help.html` c'è una galleria in formato verticale.
Per aggiungere un'immagine copia un blocco `<figure class="media">…</figure>` e cambia file e testi.
Dentro la galleria c'è un commento con i modelli pronti per **video .mp4** (da mettere in `assets/video/`)
e per **reel di Instagram**.

## Come modificare

- **Testi**: apri il file `.html` (anche su github.com, icona matita) e cambia le frasi tra i tag.
- **Menu, contatti e piè di pagina** sono uguali in tutte le pagine: si cambiano in `_strumenti/build.py`.
- **Colori**: in cima a `style.css`, sezione `:root`. I blu `--sky-1`…`--sky-6` e i bagliori vengono dalla locandina "AI help You"; `--signal` è il magenta dello scudo.
- **Logo**: lo scudo è `assets/logo-scudo.png` (sfondo trasparente); il bagliore sotto è disegnato in `style.css` (sezione "logo").
- **Link agli store e al pulsante**: cerca `play.google.com`, `apps.apple.com` o `aliexpress` nei file.
- Dopo commit e push, GitHub Pages aggiorna il sito in 1–2 minuti.

## Strumenti (per chi rigenera il sito)

```bash
python3 _strumenti/build.py                      # rigenera le 8 pagine da _strumenti/pagine/
python3 _strumenti/traduzioni.py CARTELLA en fr  # converte le traduzioni in lang/*.js e le controlla
```

`_strumenti/traduzioni/it.json` è l'elenco numerato dei testi italiani; `_strumenti/traduzioni/sorgenti/`
contiene le traduzioni riga per riga; `_strumenti/traduzioni/xx.json` è l'archivio testo italiano → traduzione.
