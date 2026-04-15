"""
Encoding scheme
===============
Instruction word (32-bit R-type):
  [31:26] opcode   — 6 bits  (all logic ops share opcode 0b000000)
  [25:21] rs       — 5 bits  (source register 1)
  [20:16] rt       — 5 bits  (source register 2)
  [15:11] rd       — 5 bits  (destination register)
  [10:6]  shamt    — 5 bits  (unused, always 0)
  [5:0]   funct    — 6 bits  (encodes AND/OR + optional invert flag)

Function field encoding (funct[5:0]):
  Bit 5   : invert_a flag  (1 = invert input A before operation)
  Bits 4:0: base operation (see ALUOp below)

Example:
  funct = 0b100100  →  invert_a=1, base_op=AND  →  (~A) & B
  funct = 0b000100  →  invert_a=0, base_op=AND  →  A & B
  funct = 0b000101  →  invert_a=0, base_op=OR   →  A | B
"""


class ALUOp:
    AND = 0b00   # 0
    OR  = 0b01   # 1


#Function-field constants
FUNCT_AND          = 0b00_0100   # 0x04  standard AND
FUNCT_AND_NOT_A    = 0b10_0100   # 0x24  AND with input-A inverted  (~A & B)
FUNCT_OR           = 0b00_0101   # 0x05  standard OR

# Masking to extract the invert-A flag from funct
INVERT_A_BIT = 5       # bit position
INVERT_A_MASK = 1 << INVERT_A_BIT   # 0b100000


def decode_funct(funct: int) -> tuple[int, bool]:
    invert_a = bool(funct & INVERT_A_MASK)
    base_op  = funct & ~INVERT_A_MASK  # strip the invert bit

    if base_op == (FUNCT_AND & ~INVERT_A_MASK):
        alu_op = ALUOp.AND
    elif base_op == (FUNCT_OR & ~INVERT_A_MASK):
        alu_op = ALUOp.OR
    else:
        raise ValueError(f"Unknown function field: {funct:#08b}")

    return alu_op, invert_a