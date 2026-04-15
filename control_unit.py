"""
Decodes a 32-bit R-type instruction and generates all control signals
required by the datapath for one clock cycle.

Control signals produced
========================
  reg_write    : bool  — assert to write result back to rd
  alu_op       : int   — ALUOp constant (AND=0, OR=1)
  invert_a     : bool  — invert ALU input A  (NOT without a separate instruction)

Instruction format expected (R-type)
=====================================
  [31:26] opcode  (6 bits) — must be 0 for logic ops
  [25:21] rs      (5 bits) — source register 1
  [20:16] rt      (5 bits) — source register 2
  [15:11] rd      (5 bits) — destination register
  [10: 6] shamt   (5 bits) — ignored
  [ 5: 0] funct   (6 bits) — selects operation + invert flag
"""

from alu_control import decode_funct
from dataclasses import dataclass


@dataclass
class ControlSignals:
    """All control signals generated for one instruction."""
    reg_write: bool
    alu_op: int          # ALUOp.AND or ALUOp.OR
    invert_a: bool       # True → invert input A in ALU
    rs: int              # source register 1 index
    rt: int              # source register 2 index
    rd: int              # destination register index
    funct: int           # raw function field (for tracing)
    opcode: int          # raw opcode (for tracing)

    def summary(self) -> str:
        op_str = "AND" if self.alu_op == 0 else "OR"
        inv_str = " [invert A]" if self.invert_a else ""
        return (
            f"opcode={self.opcode:#08b}  funct={self.funct:#08b}  "
            f"op={op_str}{inv_str}  "
            f"rs=t{self.rs}  rt=t{self.rt}  rd=t{self.rd}  "
            f"RegWrite={int(self.reg_write)}"
        )


# Supported opcode(s)
OPCODE_RTYPE = 0b000000


class ControlUnit:
    """Decodes one instruction per cycle and produces ControlSignals."""

    def decode(self, instruction: int) -> ControlSignals:
        """
        Decode *instruction* (32-bit integer) and return ControlSignals.

        Raises ValueError for unsupported opcodes.
        """
        opcode = (instruction >> 26) & 0x3F
        rs     = (instruction >> 21) & 0x1F
        rt     = (instruction >> 16) & 0x1F
        rd     = (instruction >> 11) & 0x1F
        # shamt = (instruction >>  6) & 0x1F  # unused
        funct  =  instruction        & 0x3F

        if opcode != OPCODE_RTYPE:
            raise ValueError(
                f"Unsupported opcode {opcode:#08b}. "
                "Only R-type (0b000000) logic instructions are supported."
            )

        alu_op, invert_a = decode_funct(funct)

        return ControlSignals(
            reg_write=True,
            alu_op=alu_op,
            invert_a=invert_a,
            rs=rs,
            rt=rt,
            rd=rd,
            funct=funct,
            opcode=opcode,
        )