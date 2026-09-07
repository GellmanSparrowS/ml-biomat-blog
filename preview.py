# -*- coding: utf-8 -*-
"""Local preview server. Binds all interfaces and auto-opens a browser."""
import argparse
import os
import socket
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DOCS = Path(__file__).resolve().parent / "docs"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOCS), **kwargs)

    def log_message(self, fmt, *args):
        print("[preview]", fmt % args)


def lan_ips():
    ips = set()
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None):
            ip = info[4][0]
            if ip and ip not in ("127.0.0.1", "::1"):
                ips.add(ip)
    except Exception:
        pass
    return sorted(ips)


def open_url(url):
    try:
        os.startfile(url)  # Windows native opener
    except Exception:
        webbrowser.open(url)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8866)
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()
    if not (DOCS / "index.html").exists():
        raise SystemExit("docs/index.html not found. Run: python build.py")
    httpd = ThreadingHTTPServer(("0.0.0.0", a.port), Handler)
    urls = ["http://localhost:%d/" % a.port, "http://127.0.0.1:%d/" % a.port]
    for ip in lan_ips():
        urls.append("http://%s:%d/" % (ip, a.port))
    print("Serving", DOCS)
    for u in urls:
        print("  ", u)
    if not a.no_open:
        threading.Timer(1.0, open_url, args=(urls[0],)).start()
    print("Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()