"""Serve the published Blazor output with correct MIME types.

Python's default handler does not know .wasm or .webcil, and Blazor refuses to
instantiate a WebAssembly module served as application/octet-stream. This exists so the
trimmed Release build can be exercised exactly as a static host would serve it — the
only way to catch trimming breaking System.Text.Json before deployment does.

Usage:  python _tools/serve_publish.py [port] [root]
"""

import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

EXTRA_TYPES = {
    ".wasm": "application/wasm",
    ".webcil": "application/octet-stream",
    ".dll": "application/octet-stream",
    ".blat": "application/octet-stream",
    ".dat": "application/octet-stream",
    ".pdb": "application/octet-stream",
    ".json": "application/json",
    ".js": "text/javascript",
    ".mjs": "text/javascript",
    ".css": "text/css",
}


class BlazorHandler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, **EXTRA_TYPES}

    def send_response(self, *args, **kwargs):
        super().send_response(*args, **kwargs)

    def end_headers(self):
        # Match what a static host does for a SPA: never cache the shell.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        # SPA fallback: unknown paths without a file extension serve index.html,
        # mirroring the navigation fallback a static host is configured with.
        from pathlib import Path

        target = Path(self.translate_path(self.path))
        if not target.exists() and "." not in Path(self.path).name:
            self.path = "/index.html"

        super().do_GET()

    def log_message(self, fmt, *args):
        pass  # Quiet; failures still surface through the browser.


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5210
    root = sys.argv[2] if len(sys.argv) > 2 else "publish-test/wwwroot"

    handler = partial(BlazorHandler, directory=root)
    print(f"Serving {root} on http://localhost:{port}")

    # Threaded: Blazor requests ~50 framework assets in parallel on first load, and a
    # single-threaded handler serialises them badly enough to stall a headless page load.
    ThreadingHTTPServer(("localhost", port), handler).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
