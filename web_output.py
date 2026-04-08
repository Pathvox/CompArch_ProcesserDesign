"""
Serve Memory Hierarchy simulation output in a browser.

Usage:
    python web_output.py
Then open:
    http://127.0.0.1:8000
"""

from __future__ import annotations

import html
import io
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, HTTPServer

from main import demo_basic, demo_fifo, demo_write_back


def run_all_demos() -> str:
    """Run all existing demos and capture their console output."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        demo_basic()
        demo_fifo()
        demo_write_back()
    return buf.getvalue()


def render_page(sim_output: str) -> str:
    escaped_output = html.escape(sim_output)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Memory Hierarchy Output</title>
  <style>
    :root {{
      --bg: #0b1020;
      --panel: #151f3a;
      --text: #eef4ff;
      --accent: #56d8ff;
      --line: #25345e;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: radial-gradient(circle at top left, #10214f, var(--bg));
      color: var(--text);
      font-family: "Segoe UI", Tahoma, sans-serif;
    }}
    .wrap {{
      max-width: 1200px;
      margin: 24px auto;
      padding: 0 16px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 1.8rem;
    }}
    p {{
      margin: 0 0 16px;
      color: #c7d4f8;
    }}
    .toolbar {{
      margin-bottom: 12px;
    }}
    .btn {{
      display: inline-block;
      border: 1px solid var(--line);
      background: linear-gradient(120deg, #8ef5d8, var(--accent));
      color: #031226;
      text-decoration: none;
      font-weight: 700;
      padding: 8px 12px;
      border-radius: 10px;
    }}
    pre {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 14px;
      overflow: auto;
      white-space: pre;
      line-height: 1.35;
      font-size: 0.92rem;
      margin: 0;
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <h1>Memory Hierarchy Simulation Output</h1>
    <p>This page runs the same demos as <code>main.py</code> and shows the captured output.</p>
    <div class="toolbar">
      <a class="btn" href="/">Refresh / Re-run</a>
    </div>
    <pre>{escaped_output}</pre>
  </main>
</body>
</html>
"""


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        output = run_all_demos()
        page = render_page(output).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)


def main():
    host = "127.0.0.1"
    port = 8000
    server = HTTPServer((host, port), DemoHandler)
    print(f"Serving at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
