#!/usr/bin/env python3
"""Anteprima locale del sito su http://127.0.0.1:8765

Serve i file senza cache. Accetta anche POST /__save?name=NOME e salva il corpo in
_strumenti/traduzioni/NOME.json: serve a raccogliere dal browser i testi da tradurre
(funzione NP_I18N.collect() di site.js).

Uso:  python3 _strumenti/anteprima.py
"""
import functools
import http.server
import pathlib
import urllib.parse

TOOLS = pathlib.Path(__file__).resolve().parent
SITE = TOOLS.parent
OUT = TOOLS / "traduzioni"


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        name = "".join(c for c in q.get("name", ["raccolta"])[0] if c.isalnum() or c in "-_")
        body = self.rfile.read(int(self.headers["Content-Length"]))
        (OUT / (name + ".json")).write_bytes(body)
        self.send_response(204)
        self.end_headers()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    print("Anteprima su http://127.0.0.1:8765")
    http.server.ThreadingHTTPServer(("127.0.0.1", 8765), functools.partial(Handler, directory=str(SITE))).serve_forever()
