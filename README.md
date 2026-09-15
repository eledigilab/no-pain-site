# no pAIn — sito del progetto

Sito statico pubblicato con GitHub Pages: https://eledigilab.github.io/no-pain-site/

## Pagine

| File | Contenuto |
|---|---|
| `index.html` | Il progetto: digital4help, perché serve, i sei modi di attivazione, le azioni, l'ecosistema |
| `prodotti.html` | Le app: AI help You, Proteggimi, no pAIn iOS, AIuto SOS, AI help App, AIutoSOS Apple Watch |
| `button4help.html` | Il pulsante: cos'è, cosa non è, come si usa, link d'acquisto |
| `versioni.html` | Free e Premium con la tabella di confronto completa |
| `come-funziona.html` | Modalità di attivazione, azioni, watch4help, prima configurazione |
| `ricerca.html` | Tecnologia, pubblicazioni, presentazione PDF |
| `collabora.html` | Proposte per enti pubblici, associazioni, aziende |
| `domande.html` | Domande frequenti |
| `style.css` | Colori, caratteri e impaginazione di tutte le pagine |
| `site.js` | Menu su telefono e anno nel piè di pagina |
| `assets/` | Immagini, icona e presentazione PDF |

## Come modificare

- **Testi**: apri il file `.html` (anche direttamente su github.com, icona matita) e cambia le frasi tra i tag.
- **Menu, contatti e piè di pagina** sono ripetuti uguali in tutte le 8 pagine: se li cambi, cambiali in ognuna.
- **Colori**: in cima a `style.css`, sezione `:root` (es. `--signal` è il rosa dell'allarme).
- **Link agli store e al beacon**: cerca `play.google.com`, `apps.apple.com` o `aliexpress` nei file.
- **Immagini**: metti il file nella cartella `assets/` e usa `<img src="assets/nome-file.jpg" alt="descrizione">`.
- Dopo commit e push, GitHub Pages aggiorna il sito in 1–2 minuti.
