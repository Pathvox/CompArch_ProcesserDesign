"""
Single-Cycle Processor
CSC 4210 Computer Architecture, Spring 2026
Bollapalli Vishnavi Abhishikta
"""

import json
import os
import sys
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from processorr import Processor

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def run_case(label: str, A: int, B: int, C: int, D: int) -> dict:
    """Run the processor with one set of inputs, show results, and return trace data."""
    print(f"\n{'='*68}")
    print(f"  TEST CASE: {label}")
    print(f"  Inputs: A={A}, B={B}, C={C}, D={D}")
    print(
        "  Expected: Y = (A&B) | ((~C)&D) = "
        f"({A}&{B}) | ({(~C)&1}&{D}) = {(A & B) | ((~C & 1) & D)}"
    )
    print(f"{'='*68}")

    cpu = Processor()
    cpu.load_registers({0: A, 1: B, 2: C, 3: D})
    cpu.run(verbose=True)

    y = cpu.result()
    expected = (A & B) | ((~C & 1) & D)

    status = "PASS" if y == expected else "FAIL"
    print(f"  Validation: Y={y}  expected={expected}  {status}\n")

    serializable_trace = []
    for step in cpu.trace():
        sig = step["signals"]
        dbg = step["alu_debug"]
        serializable_trace.append(
            {
                "pc": step["pc"],
                "instr_hex": step["instr_hex"],
                "rd": step["rd"],
                "result": step["result"],
                "signals": {
                    "reg_write": sig.reg_write,
                    "alu_op": sig.alu_op,
                    "invert_a": sig.invert_a,
                    "rs": sig.rs,
                    "rt": sig.rt,
                    "rd": sig.rd,
                    "funct": sig.funct,
                    "opcode": sig.opcode,
                },
                "alu_debug": {
                    "input_a_raw": dbg["input_a_raw"],
                    "invert_a": dbg["invert_a"],
                    "input_a_effective": dbg["input_a_effective"],
                    "input_b": dbg["input_b"],
                    "alu_op": dbg["alu_op"],
                    "result": dbg["result"],
                },
            }
        )

    return {
        "label": label,
        "inputs": {"A": A, "B": B, "C": C, "D": D},
        "expected": expected,
        "output": y,
        "passed": (y == expected),
        "trace": serializable_trace,
    }


def export_visualizer_results(cases: list[dict]) -> None:
    payload = {"cases": cases}
    out_path = os.path.join(os.path.dirname(__file__), "task4_results.js")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("window.MMAIN_RESULTS = ")
        json.dump(payload, f, indent=2)
        f.write(";\n")
    print(f"  Visualizer data written to: {out_path}")


def serve_visualizer() -> None:
    base_dir = os.path.dirname(__file__)
    host = "127.0.0.1"
    port = 8000
    handler = partial(SimpleHTTPRequestHandler, directory=base_dir)
    server = ThreadingHTTPServer((host, port), handler)
    url = f"http://{host}:{port}/visualizer_task4.html"
    print(f"  Opening visualizer: {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    print("  Press Ctrl+C to stop the web server.")
    server.serve_forever()


if __name__ == "__main__":
    results = [
        run_case("A=1 B=1 C=0 D=1  ->  Y=1", A=1, B=1, C=0, D=1),
        run_case("A=0 B=1 C=1 D=1  ->  Y=0", A=0, B=1, C=1, D=1),
        run_case("A=1 B=0 C=1 D=0  ->  Y=0", A=1, B=0, C=1, D=0),
        run_case("A=1 B=1 C=1 D=1  ->  Y=1", A=1, B=1, C=1, D=1),
        run_case("A=0 B=0 C=0 D=1  ->  Y=1", A=0, B=0, C=0, D=1),
    ]
    export_visualizer_results(results)
    serve_visualizer()
