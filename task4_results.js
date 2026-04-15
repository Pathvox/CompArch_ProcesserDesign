window.MMAIN_RESULTS = {
  "cases": [
    {
      "label": "A=1 B=1 C=0 D=1  ->  Y=1",
      "inputs": {
        "A": 1,
        "B": 1,
        "C": 0,
        "D": 1
      },
      "expected": 1,
      "output": 1,
      "passed": true,
      "trace": [
        {
          "pc": 0,
          "instr_hex": "0x00012004",
          "rd": 4,
          "result": 1,
          "signals": {
            "reg_write": true,
            "alu_op": 0,
            "invert_a": false,
            "rs": 0,
            "rt": 1,
            "rd": 4,
            "funct": 4,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 1,
            "invert_a": false,
            "input_a_effective": 1,
            "input_b": 1,
            "alu_op": "AND",
            "result": 1
          }
        },
        {
          "pc": 1,
          "instr_hex": "0x00433024",
          "rd": 6,
          "result": 1,
          "signals": {
            "reg_write": true,
            "alu_op": 0,
            "invert_a": true,
            "rs": 2,
            "rt": 3,
            "rd": 6,
            "funct": 36,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 0,
            "invert_a": true,
            "input_a_effective": 4294967295,
            "input_b": 1,
            "alu_op": "AND-NOT",
            "result": 1
          }
        },
        {
          "pc": 2,
          "instr_hex": "0x00860005",
          "rd": 0,
          "result": 1,
          "signals": {
            "reg_write": true,
            "alu_op": 1,
            "invert_a": false,
            "rs": 4,
            "rt": 6,
            "rd": 0,
            "funct": 5,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 1,
            "invert_a": false,
            "input_a_effective": 1,
            "input_b": 1,
            "alu_op": "OR",
            "result": 1
          }
        }
      ]
    },
    {
      "label": "A=0 B=1 C=1 D=1  ->  Y=0",
      "inputs": {
        "A": 0,
        "B": 1,
        "C": 1,
        "D": 1
      },
      "expected": 0,
      "output": 0,
      "passed": true,
      "trace": [
        {
          "pc": 0,
          "instr_hex": "0x00012004",
          "rd": 4,
          "result": 0,
          "signals": {
            "reg_write": true,
            "alu_op": 0,
            "invert_a": false,
            "rs": 0,
            "rt": 1,
            "rd": 4,
            "funct": 4,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 0,
            "invert_a": false,
            "input_a_effective": 0,
            "input_b": 1,
            "alu_op": "AND",
            "result": 0
          }
        },
        {
          "pc": 1,
          "instr_hex": "0x00433024",
          "rd": 6,
          "result": 0,
          "signals": {
            "reg_write": true,
            "alu_op": 0,
            "invert_a": true,
            "rs": 2,
            "rt": 3,
            "rd": 6,
            "funct": 36,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 1,
            "invert_a": true,
            "input_a_effective": 4294967294,
            "input_b": 1,
            "alu_op": "AND-NOT",
            "result": 0
          }
        },
        {
          "pc": 2,
          "instr_hex": "0x00860005",
          "rd": 0,
          "result": 0,
          "signals": {
            "reg_write": true,
            "alu_op": 1,
            "invert_a": false,
            "rs": 4,
            "rt": 6,
            "rd": 0,
            "funct": 5,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 0,
            "invert_a": false,
            "input_a_effective": 0,
            "input_b": 0,
            "alu_op": "OR",
            "result": 0
          }
        }
      ]
    },
    {
      "label": "A=1 B=0 C=1 D=0  ->  Y=0",
      "inputs": {
        "A": 1,
        "B": 0,
        "C": 1,
        "D": 0
      },
      "expected": 0,
      "output": 0,
      "passed": true,
      "trace": [
        {
          "pc": 0,
          "instr_hex": "0x00012004",
          "rd": 4,
          "result": 0,
          "signals": {
            "reg_write": true,
            "alu_op": 0,
            "invert_a": false,
            "rs": 0,
            "rt": 1,
            "rd": 4,
            "funct": 4,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 1,
            "invert_a": false,
            "input_a_effective": 1,
            "input_b": 0,
            "alu_op": "AND",
            "result": 0
          }
        },
        {
          "pc": 1,
          "instr_hex": "0x00433024",
          "rd": 6,
          "result": 0,
          "signals": {
            "reg_write": true,
            "alu_op": 0,
            "invert_a": true,
            "rs": 2,
            "rt": 3,
            "rd": 6,
            "funct": 36,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 1,
            "invert_a": true,
            "input_a_effective": 4294967294,
            "input_b": 0,
            "alu_op": "AND-NOT",
            "result": 0
          }
        },
        {
          "pc": 2,
          "instr_hex": "0x00860005",
          "rd": 0,
          "result": 0,
          "signals": {
            "reg_write": true,
            "alu_op": 1,
            "invert_a": false,
            "rs": 4,
            "rt": 6,
            "rd": 0,
            "funct": 5,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 0,
            "invert_a": false,
            "input_a_effective": 0,
            "input_b": 0,
            "alu_op": "OR",
            "result": 0
          }
        }
      ]
    },
    {
      "label": "A=1 B=1 C=1 D=1  ->  Y=1",
      "inputs": {
        "A": 1,
        "B": 1,
        "C": 1,
        "D": 1
      },
      "expected": 1,
      "output": 1,
      "passed": true,
      "trace": [
        {
          "pc": 0,
          "instr_hex": "0x00012004",
          "rd": 4,
          "result": 1,
          "signals": {
            "reg_write": true,
            "alu_op": 0,
            "invert_a": false,
            "rs": 0,
            "rt": 1,
            "rd": 4,
            "funct": 4,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 1,
            "invert_a": false,
            "input_a_effective": 1,
            "input_b": 1,
            "alu_op": "AND",
            "result": 1
          }
        },
        {
          "pc": 1,
          "instr_hex": "0x00433024",
          "rd": 6,
          "result": 0,
          "signals": {
            "reg_write": true,
            "alu_op": 0,
            "invert_a": true,
            "rs": 2,
            "rt": 3,
            "rd": 6,
            "funct": 36,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 1,
            "invert_a": true,
            "input_a_effective": 4294967294,
            "input_b": 1,
            "alu_op": "AND-NOT",
            "result": 0
          }
        },
        {
          "pc": 2,
          "instr_hex": "0x00860005",
          "rd": 0,
          "result": 1,
          "signals": {
            "reg_write": true,
            "alu_op": 1,
            "invert_a": false,
            "rs": 4,
            "rt": 6,
            "rd": 0,
            "funct": 5,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 1,
            "invert_a": false,
            "input_a_effective": 1,
            "input_b": 0,
            "alu_op": "OR",
            "result": 1
          }
        }
      ]
    },
    {
      "label": "A=0 B=0 C=0 D=1  ->  Y=1",
      "inputs": {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 1
      },
      "expected": 1,
      "output": 1,
      "passed": true,
      "trace": [
        {
          "pc": 0,
          "instr_hex": "0x00012004",
          "rd": 4,
          "result": 0,
          "signals": {
            "reg_write": true,
            "alu_op": 0,
            "invert_a": false,
            "rs": 0,
            "rt": 1,
            "rd": 4,
            "funct": 4,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 0,
            "invert_a": false,
            "input_a_effective": 0,
            "input_b": 0,
            "alu_op": "AND",
            "result": 0
          }
        },
        {
          "pc": 1,
          "instr_hex": "0x00433024",
          "rd": 6,
          "result": 1,
          "signals": {
            "reg_write": true,
            "alu_op": 0,
            "invert_a": true,
            "rs": 2,
            "rt": 3,
            "rd": 6,
            "funct": 36,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 0,
            "invert_a": true,
            "input_a_effective": 4294967295,
            "input_b": 1,
            "alu_op": "AND-NOT",
            "result": 1
          }
        },
        {
          "pc": 2,
          "instr_hex": "0x00860005",
          "rd": 0,
          "result": 1,
          "signals": {
            "reg_write": true,
            "alu_op": 1,
            "invert_a": false,
            "rs": 4,
            "rt": 6,
            "rd": 0,
            "funct": 5,
            "opcode": 0
          },
          "alu_debug": {
            "input_a_raw": 0,
            "invert_a": false,
            "input_a_effective": 0,
            "input_b": 1,
            "alu_op": "OR",
            "result": 1
          }
        }
      ]
    }
  ]
};
