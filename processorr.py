"""
Integrates all datapath components and drives a single-cycle execution loop:
    Fetch → Decode → Execute → Write-back

Components Used here
=============================
  InstructionMemory  — holds the encoded program
  RegisterFile       — 8 × 32-bit registers (t0–t7)
  ControlUnit        — decodes instructions → control signals
  ALU                — executes AND / OR (with optional invert)
  MUX                — routes ALU inputs as directed by control signals
"""

import sys
import os

# Allow imports from the same src/ directory
sys.path.insert(0, os.path.dirname(__file__))

from instruction_memory import InstructionMemory
from register_file       import RegisterFile
from control_unit        import ControlUnit
from Alu                 import ALU
from mux                 import mux2          # reserved for future extensions


_SEP = "─" * 68


class Processor:
    """Single-cycle 32-bit processor executing AND/OR/AND-NOT programs."""

    def __init__(self):
        self.imem    = InstructionMemory.from_program()
        self.regfile = RegisterFile()
        self.ctrl    = ControlUnit()
        self.alu     = ALU()
        self.pc      = 0                 # program counter (word address)
        self._trace: list[dict] = []     # execution trace

    
    def load_registers(self, values: dict[int, int]) -> None:
        """Load initial register values.  keys are register indices (0–7)."""
        self.regfile.load(values)

    def run(self, verbose: bool = True) -> None:
        """Execute the full program and optionally print a detailed trace."""
        self.pc = 0
        self._trace.clear()

        if verbose:
            print(_SEP)
            print("  Single-Cycle Processor — Execution Trace")
            print(_SEP)
            self._print_registers("Initial register state")

        while self.pc < len(self.imem):
            record = self._execute_one(verbose)
            self._trace.append(record)

        if verbose:
            self._print_registers("Final register state")
            print(_SEP)
            self._print_result()

    def result(self) -> int:
        """Return the final value of t0  (Y = A·B + C'·D)."""
        return self.regfile.read(0)

    def trace(self) -> list[dict]:
        """Return the execution trace (one dict per instruction)."""
        return list(self._trace)

    
    # Internal: single-cycle pipeline stages

    def _execute_one(self, verbose: bool) -> dict:
        # 1. FETCHING
        instruction = self.imem.fetch(self.pc)

        # 2. DECODING 
        signals = self.ctrl.decode(instruction)

        # 3. EXECUTING
        #   MUX selects rs and rt as ALU inputs (select=0 → direct read)
        val_rs = mux2(self.regfile.read(signals.rs), 0, select=0)
        val_rt = mux2(self.regfile.read(signals.rt), 0, select=0)

        result, alu_debug = self.alu.execute(
            input_a  = val_rs,
            input_b  = val_rt,
            alu_op   = signals.alu_op,
            invert_a = signals.invert_a,
        )

        # 4. WRITE-BACK 
        self.regfile.write(signals.rd, result, write_enable=signals.reg_write)

        self.pc += 1

        record = {
            "pc":         self.pc - 1,
            "instr_hex":  f"0x{instruction:08X}",
            "signals":    signals,
            "alu_debug":  alu_debug,
            "rd":         signals.rd,
            "result":     result,
        }

        if verbose:
            self._print_step(record)

        return record

    @staticmethod
    def _reg_name(idx: int) -> str:
        return f"t{idx}"

    def _print_registers(self, label: str) -> None:
        print(f"\n  {label}:")
        dump = self.regfile.dump()
        pairs = [f"  {k}={v}" for k, v in dump.items() if v != 0
                 or int(k[1:]) <= 6]
        print("  " + "  ".join(pairs))
        print()

    def _print_step(self, r: dict) -> None:
        sig   = r["signals"]
        dbg   = r["alu_debug"]
        pc    = r["pc"]
        op    = dbg["alu_op"]
        rd    = self._reg_name(r["rd"])
        rs    = self._reg_name(sig.rs)
        rt    = self._reg_name(sig.rt)
        a_eff = dbg["input_a_effective"]
        b_val = dbg["input_b"]
        res   = r["result"]

        print(f"  PC={pc}  [{r['instr_hex']}]  {op}  {rd} ← {rs}, {rt}")
        print(f"         Control : {sig.summary()}")
        print(f"         ALU in  : A_eff={a_eff:#010x}  B={b_val:#010x}")
        print(f"         ALU out : {res:#010x}  ({res})")
        print(f"         Writeback: {rd} ← {res:#010x}")
        print()

    def _print_result(self) -> None:
        y = self.result()
        print(f"  Final Output  Y = t0 = {y:#010x}  (decimal {y})")
        print()
        # Intermediate values from trace
        if len(self._trace) >= 3:
            t4 = self._trace[0]["result"]
            t6 = self._trace[1]["result"]
            print(f"  Intermediate values:")
            print(f"    t4 = A & B        = {t4:#010x}  ({t4})")
            print(f"    t6 = (~C) & D     = {t6:#010x}  ({t6})")
            print(f"    t0 = t4 | t6  (Y) = {y:#010x}  ({y})")
        print(_SEP)
