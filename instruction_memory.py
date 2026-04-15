"""
Encodes assembly-level instructions into 32-bit machine words and
provides a simple instruction-memory store that the processor fetches from.

Instruction format (R-type)
============================
  [31:26]  opcode  = 0b000000  (all logic ops are R-type)
  [25:21]  rs      = source register 1
  [20:16]  rt      = source register 2
  [15:11]  rd      = destination register
  [10: 6]  shamt   = 0 (unused)
  [ 5: 0]  funct   = operation code  (see alu_control.py)

Supported assembly mnemonics
=============================
  and  rd, rs, rt       →  funct = FUNCT_AND
  andn rd, rs, rt       →  funct = FUNCT_AND_NOT_A  (invert rs)
  or   rd, rs, rt       →  funct = FUNCT_OR
"""

from alu_control import FUNCT_AND, FUNCT_AND_NOT_A, FUNCT_OR

# R-type opcode
_OPCODE_RTYPE = 0b000000


def _rtype(opcode: int, rs: int, rt: int, rd: int, shamt: int, funct: int) -> int:
    """Pack fields into a 32-bit R-type instruction word."""
    return (
        ((opcode & 0x3F) << 26) |
        ((rs     & 0x1F) << 21) |
        ((rt     & 0x1F) << 16) |
        ((rd     & 0x1F) << 11) |
        ((shamt  & 0x1F) <<  6) |
        ( funct  & 0x3F)
    )


def encode_and(rd: int, rs: int, rt: int) -> int:
    """Encode  AND rd, rs, rt"""
    return _rtype(_OPCODE_RTYPE, rs, rt, rd, 0, FUNCT_AND)


def encode_andn(rd: int, rs: int, rt: int) -> int:
    """Encode  AND-NOT-A rd, rs, rt  (result = (~rs) & rt)"""
    return _rtype(_OPCODE_RTYPE, rs, rt, rd, 0, FUNCT_AND_NOT_A)


def encode_or(rd: int, rs: int, rt: int) -> int:
    """Encode  OR rd, rs, rt"""
    return _rtype(_OPCODE_RTYPE, rs, rt, rd, 0, FUNCT_OR)


class InstructionMemory:

    def __init__(self, instructions: list[int]):
        self._mem = list(instructions)

    def fetch(self, pc: int) -> int:
        if not (0 <= pc < len(self._mem)):
            raise IndexError(f"PC {pc} out of instruction memory range.")
        return self._mem[pc]

    def __len__(self) -> int:
        return len(self._mem)

    @staticmethod
    def from_program() -> "InstructionMemory":
        t0, t1, t2, t3, t4, t6 = 0, 1, 2, 3, 4, 6

        instructions = [
            encode_and (t4, t0, t1),   # and  t4, t0, t1
            encode_andn(t6, t2, t3),   # andn t6, t2, t3  (invert t2=C)
            encode_or  (t0, t4, t6),   # or   t0, t4, t6
        ]
        return InstructionMemory(instructions)