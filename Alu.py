"""
Supported operations (selected by *alu_op*):
  0b00  AND  — bitwise AND, optionally with input-A inversion
  0b01  OR   — bitwise OR

The NOT operation is NOT a separate instruction.  Instead, the control
unit asserts *invert_a* to negate ALU input A before the AND gate,
realising   result = (~A) & B.
"""

from alu_control import ALUOp


class ALU:
    """32-bit ALU supporting AND, OR, and conditional input inversion."""

    MASK32 = 0xFFFF_FFFF

    def execute(
        self,
        input_a: int,
        input_b: int,
        alu_op: int,
        invert_a: bool = False,
    ) -> tuple[int, dict]:
        
        a = input_a & self.MASK32
        b = input_b & self.MASK32

        # inversion of input A
        a_effective = (~a) & self.MASK32 if invert_a else a

        # Operation selection 
        if alu_op == ALUOp.AND:
            result = a_effective & b
            op_name = "AND-NOT" if invert_a else "AND"
        elif alu_op == ALUOp.OR:
            result = a_effective | b
            op_name = "OR-NOT-A" if invert_a else "OR"
        else:
            raise ValueError(f"Unknown ALU op: {alu_op:#04b}")

        result &= self.MASK32

        debug = {
            "input_a_raw": a,
            "invert_a": invert_a,
            "input_a_effective": a_effective,
            "input_b": b,
            "alu_op": op_name,
            "result": result,
        }
        return result, debug