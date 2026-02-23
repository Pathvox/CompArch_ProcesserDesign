# Bollapalli Vishnavi Abhishikta
# Processor Design Project
#Task 1: Data Systems conversion logic and constraints.

class ProcessorDataSystem:
    def __init__(self):
        # FR2: The processor is a 32-bit signed integer 
        # The valid representable range: -2,147,483,648 to 2,147,483,647
        self.MIN_INT32 = -2147483648
        self.MAX_INT32 = 2147483647

    def process_input(self, decimal_input, format_selector): #Handles conversion, overflow detection, and saturation
        overflow = 0
        saturated = 0
        internal_value = decimal_input

        # FR4 & FR5: Range or Overflow Detection and Saturation Policy 
        # If the input exceeds limits, clamp saturate to the boundary
        if decimal_input > self.MAX_INT32:
            internal_value = self.MAX_INT32
            overflow = 1
            saturated = 1
        elif decimal_input < self.MIN_INT32:
            internal_value = self.MIN_INT32
            overflow = 1
            saturated = 1

        # FR3: Internal 32-bit Two's Complement 
        # masking with 0xFFFFFFFF ensures a 32-bit representation
        binary_32 = format(internal_value & 0xFFFFFFFF, '032b')

        # FR6: Output Formatting (DEC, BIN, or HEX)
        value_out = ""
        if format_selector == "DEC":
            value_out = str(internal_value) # signed decimal 
        elif format_selector == "BIN":
            value_out = binary_32 # 32-bit binary string
        elif format_selector == "HEX":
            value_out = format(internal_value & 0xFFFFFFFF, '08X') # 8-digit hexadecimal
        
        # FR7: Status Output 
        return {
            "value_out": value_out,
            "overflow": overflow,
            "saturated": saturated
        }

def run_task1_demo():
    """
    Demonstrates the system with mandatory test cases.
    """
    pds = ProcessorDataSystem()
    
    # FR8: Required Tests 
    test_cases = [
        (123, "DEC", "Positive number"),
        (0, "BIN", "Zero"),
        (-123, "HEX", "Negative number"),
        (2147483647, "DEC", "MAX_INT32"),
        (-2147483648, "BIN", "MIN_INT32"),
        (2147483648, "DEC", "Overflow (MAX+1)"),
        (-2147483649, "HEX", "Overflow (MIN-1)")
    ]

    print(f"{'Condition':<20} | {'Input':<12} | {'Output':<32} | {'OV':<2} | {'SAT':<2}")
    print("-" * 80)
    
    for val, fmt, desc in test_cases:
        res = pds.process_input(val, fmt)
        print(f"{desc:<20} | {val:<12} | {res['value_out']:<32} | {res['overflow']:<2} | {res['saturated']:<2}")

if __name__ == "__main__":
    run_task1_demo()
