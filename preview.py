# -*- coding: utf-8 -*-
"""Local preview server for docs/ (visual confirmation before any publish).

Usage:
  python preview.py [--port 8866] [--no-open]
"""
import argparse
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8866)
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()
    if not (DOCS / "index.html").exists():
        raise SystemExit("docs/index.html not found. Run: python build.py")
    url = "http://127.0.0.1:%d/" % a.port
    httpd = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    if not a.no_open:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    print("Serving", DOCS, "at", url, "(Ctrl+C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()