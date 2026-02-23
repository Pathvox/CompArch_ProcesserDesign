import unittest
from processor import ProcessorDataSystem

class TestProcessorDataSystem(unittest.TestCase):
    def setUp(self):
        self.pds = ProcessorDataSystem()

    def test_positive_value(self):
        # FR8.1: positive numbers
        res = self.pds.process_input(123, "DEC")
        self.assertEqual(res["value_out"], "123")
        self.assertEqual(res["overflow"], 0)
        self.assertEqual(res["saturated"], 0)

    def test_zero(self):
        # FR8.2: Zero (0)
        res = self.pds.process_input(0, "BIN")
        self.assertEqual(res["value_out"], "0" * 32)
        self.assertEqual(res["overflow"], 0)

    def test_negative_value(self):
        # FR8.3: negative numbers
        res = self.pds.process_input(-123, "HEX")
        # Two's complement of -123 in 32-bit hexadeciaml is FFFFFF85
        self.assertEqual(res["value_out"], "FFFFFF85")
        self.assertEqual(res["overflow"], 0)

    def test_boundaries(self):
        # FR8.4: Boundaries (MAX_INT32, MIN_INT32)
        max_res = self.pds.process_input(2147483647, "DEC")
        min_res = self.pds.process_input(-2147483648, "DEC")
        
        self.assertEqual(max_res["value_out"], "2147483647")
        self.assertEqual(max_res["overflow"], 0)
        self.assertEqual(min_res["value_out"], "-2147483648")
        self.assertEqual(min_res["overflow"], 0)

    def test_overflow_high(self):
        # FR8.5: Overflow - (MAX_INT32 + 1)
        # Then should saturate to MAX_INT32
        res = self.pds.process_input(2147483648, "DEC")
        self.assertEqual(res["value_out"], "2147483647")
        self.assertEqual(res["overflow"], 1)
        self.assertEqual(res["saturated"], 1)

    def test_overflow_low(self):
        # FR8.5: Overflow - (MIN_INT32 - 1)
        # Then should saturate to MIN_INT32
        res = self.pds.process_input(-2147483649, "DEC")
        self.assertEqual(res["value_out"], "-2147483648")
        self.assertEqual(res["overflow"], 1)
        self.assertEqual(res["saturated"], 1)

if __name__ == "__main__":
    unittest.main()
