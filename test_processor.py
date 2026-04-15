"""
Run with:   python -m pytest tests/test_processor.py -v
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from register_file      import RegisterFile
from alu                import ALU
from alu_control        import ALUOp, decode_funct, FUNCT_AND, FUNCT_AND_NOT_A, FUNCT_OR
from control_unit       import ControlUnit
from instruction_memory import InstructionMemory, encode_and, encode_andn, encode_or
from mux                import mux2, muxN

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from processor import Processor


# RegisterFile

class TestRegisterFile:
    def test_initial_values_zero(self):
        rf = RegisterFile()
        for i in range(8):
            assert rf.read(i) == 0

    def test_write_and_read(self):
        rf = RegisterFile()
        rf.write(3, 0xDEAD_BEEF)
        assert rf.read(3) == 0xDEAD_BEEF

    def test_write_enable_false(self):
        rf = RegisterFile()
        rf.write(2, 0xFF, write_enable=False)
        assert rf.read(2) == 0

    def test_mask_to_32_bits(self):
        rf = RegisterFile()
        rf.write(0, 0x1_FFFF_FFFF)   # 33-bit value
        assert rf.read(0) == 0xFFFF_FFFF

    def test_invalid_register(self):
        rf = RegisterFile()
        with pytest.raises(ValueError):
            rf.read(8)


# ALU 
class TestALU:
    def setup_method(self):
        self.alu = ALU()

    def test_and_basic(self):
        result, _ = self.alu.execute(0b1100, 0b1010, ALUOp.AND)
        assert result == 0b1000

    def test_or_basic(self):
        result, _ = self.alu.execute(0b1100, 0b1010, ALUOp.OR)
        assert result == 0b1110

    def test_and_with_invert_a(self):
        # (~0b1100) & 0b1111 = 0b0011 & 0b1111 = 0b0011
        result, _ = self.alu.execute(0b1100, 0b1111, ALUOp.AND, invert_a=True)
        assert result & 0xF == 0b0011

    def test_mask_32_bits(self):
        result, _ = self.alu.execute(0xFFFF_FFFF, 0xFFFF_FFFF, ALUOp.AND)
        assert result == 0xFFFF_FFFF

    def test_invalid_op(self):
        with pytest.raises(ValueError):
            self.alu.execute(1, 1, 0b11)


# ALU Control

class TestALUControl:
    def test_decode_and(self):
        op, inv = decode_funct(FUNCT_AND)
        assert op == ALUOp.AND and not inv

    def test_decode_and_not(self):
        op, inv = decode_funct(FUNCT_AND_NOT_A)
        assert op == ALUOp.AND and inv

    def test_decode_or(self):
        op, inv = decode_funct(FUNCT_OR)
        assert op == ALUOp.OR and not inv


# Control Unit

class TestControlUnit:
    def setup_method(self):
        self.cu = ControlUnit()

    def test_and_instruction(self):
        instr = encode_and(4, 0, 1)   # and t4, t0, t1
        sig = self.cu.decode(instr)
        assert sig.alu_op == ALUOp.AND
        assert not sig.invert_a
        assert sig.rd == 4
        assert sig.rs == 0
        assert sig.rt == 1
        assert sig.reg_write

    def test_andn_instruction(self):
        instr = encode_andn(6, 2, 3)  # andn t6, t2, t3
        sig = self.cu.decode(instr)
        assert sig.alu_op == ALUOp.AND
        assert sig.invert_a

    def test_or_instruction(self):
        instr = encode_or(0, 4, 6)    # or t0, t4, t6
        sig = self.cu.decode(instr)
        assert sig.alu_op == ALUOp.OR
        assert not sig.invert_a


# MUX

class TestMux:
    def test_mux2_select_0(self):
        assert mux2(42, 99, 0) == 42

    def test_mux2_select_1(self):
        assert mux2(42, 99, 1) == 99

    def test_muxN(self):
        assert muxN([10, 20, 30], 2) == 30


# Full Processor Integration

class TestProcessor:

    def _run(self, A, B, C, D):
        cpu = Processor()
        cpu.load_registers({0: A, 1: B, 2: C, 3: D})
        cpu.run(verbose=False)
        return cpu

    def _expected(self, A, B, C, D):
        return (A & B) | ((~C & 1) & D)

    @pytest.mark.parametrize("A,B,C,D", [
        (1, 1, 0, 1),   # Y=1
        (0, 1, 1, 1),   # Y=0
        (1, 0, 1, 0),   # Y=0
        (1, 1, 1, 1),   # Y=1  (A&B=1, C'&D=0, Y=1)
        (0, 0, 0, 1),   # Y=1  (A&B=0, C'&D=1, Y=1)
        (0, 0, 1, 0),   # Y=0
    ])
    def test_boolean_expression(self, A, B, C, D):
        cpu = self._run(A, B, C, D)
        assert cpu.result() == self._expected(A, B, C, D), (
            f"A={A} B={B} C={C} D={D}: "
            f"got {cpu.result()}, expected {self._expected(A,B,C,D)}"
        )

    def test_trace_has_three_steps(self):
        cpu = self._run(1, 1, 0, 1)
        assert len(cpu.trace()) == 3

    def test_intermediate_t4(self):
        cpu = self._run(1, 1, 0, 1)
        assert cpu.trace()[0]["result"] == 1   # t4 = A & B = 1

    def test_intermediate_t6(self):
        cpu = self._run(1, 1, 0, 1)
        assert cpu.trace()[1]["result"] == 1   # t6 = (~C) & D = 1