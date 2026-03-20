import argparse
import itertools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, List, Sequence, Tuple
import webbrowser

APP_NAME = "The Minterm Matrix"


def variable_names(n: int) -> List[str]:
    return [chr(65 + i) for i in range(n)]


def generate_combinations(n: int) -> List[Tuple[int, ...]]:
    return list(itertools.product([0, 1], repeat=n))


def truth_rows_from_outputs(n: int, outputs: Sequence[int]) -> List[Dict[str, Tuple[int, ...] | int]]:
    combos = generate_combinations(n)
    if len(outputs) != len(combos):
        raise ValueError(f"Expected {len(combos)} outputs for {n} variables.")

    rows = []
    for combo, out in zip(combos, outputs):
        bit = 1 if int(out) == 1 else 0
        rows.append({"inputs": combo, "output": bit})
    return rows


def canonical_sop(rows: Sequence[Dict[str, Tuple[int, ...] | int]]) -> Dict[str, List[int] | str]:
    if not rows:
        return {"minterms": [], "sop": "0"}

    n = len(rows[0]["inputs"])  # type: ignore[index]
    vars_ = variable_names(n)
    minterms: List[int] = []
    terms: List[str] = []

    for i, row in enumerate(rows):
        out = int(row["output"])  # type: ignore[arg-type]
        if out == 1:
            minterms.append(i)
            bits = row["inputs"]  # type: ignore[assignment]
            term = "".join(var if bit == 1 else f"{var}'" for bit, var in zip(bits, vars_))
            terms.append(term)

    return {"minterms": minterms, "sop": " + ".join(terms) if terms else "0"}


def kmap_grid(rows: Sequence[Dict[str, Tuple[int, ...] | int]], n: int) -> Dict[str, Sequence[Sequence[int] | str]]:
    table = {tuple(row["inputs"]): int(row["output"]) for row in rows}  # type: ignore[arg-type]

    if n == 2:
        headers = ["A\\B", "0", "1"]
        body = [
            ["0", table[(0, 0)], table[(0, 1)]],
            ["1", table[(1, 0)], table[(1, 1)]],
        ]
        return {"headers": headers, "body": body}

    gray2 = [(0, 0), (0, 1), (1, 1), (1, 0)]
    if n == 3:
        headers = ["A\\BC", "00", "01", "11", "10"]
        body = []
        for a in (0, 1):
            row = [str(a)]
            for b, c in gray2:
                row.append(table[(a, b, c)])
            body.append(row)
        return {"headers": headers, "body": body}

    if n == 4:
        headers = ["AB\\CD", "00", "01", "11", "10"]
        body = []
        for a, b in gray2:
            row = [f"{a}{b}"]
            for c, d in gray2:
                row.append(table[(a, b, c, d)])
            body.append(row)
        return {"headers": headers, "body": body}

    raise ValueError("K-map is supported for 2, 3, or 4 variables.")


def run_server(port: int, open_browser: bool = True) -> None:
    web_dir = Path(__file__).resolve().parent / "web"
    if not web_dir.exists():
        raise FileNotFoundError("Missing web directory. Expected: ./web/index.html")

    handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, directory=str(web_dir), **kwargs)
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    url = f"http://127.0.0.1:{port}"

    print(f"{APP_NAME} web app is running at {url}")
    print("Press Ctrl+C to stop the server.")

    if open_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Run {APP_NAME} web app")
    parser.add_argument("--port", type=int, default=8000, help="Port number (default: 8000)")
    parser.add_argument("--no-browser", action="store_true", help="Do not auto-open browser")
    args = parser.parse_args()

    run_server(port=args.port, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()
