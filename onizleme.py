#!/usr/bin/env python3
# Sofilx LOTO - yerel önizleme sunucusu (temiz URL + önbelleksiz)
import http.server, os, sys, urllib.parse, webbrowser, threading
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def end_headers(s):
        s.send_header('Cache-Control', 'no-store'); super().end_headers()
    def translate_path(s, path):
        p = urllib.parse.unquote(path.split('?')[0].split('#')[0])
        full = os.path.join(ROOT, p.lstrip('/'))
        if p == '/': return os.path.join(ROOT, 'index.html')
        if os.path.isfile(full.rstrip('/') + '.html'): return full.rstrip('/') + '.html'
        return full
    def send_error(s, code, message=None, explain=None):
        if code == 404:
            s.send_response(404); s.send_header('Content-Type', 'text/html; charset=utf-8'); s.end_headers()
            s.wfile.write(open(os.path.join(ROOT, '404.html'), 'rb').read()); return
        super().send_error(code, message, explain)
    def log_message(s, *a): pass
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8766
srv = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H)
if '--no-browser' not in sys.argv:
    threading.Timer(1, lambda: webbrowser.open(f'http://localhost:{PORT}/')).start()
print(f'Önizleme: http://localhost:{PORT}/  (kapatmak için Ctrl+C)')
srv.serve_forever()
