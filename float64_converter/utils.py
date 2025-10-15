"""
utils.py

Helper functions for displaying and testing IEEE 754 
64-bit floating point representations.
"""

def display_components(bits):
    """
    Print the sign, eleven_bits , and fiftytwo_bits from a 64-bit binary string.
    """
    if len(bits) != 64 or any(b not in "01" for b in bits):
        print("Error: Input must be a 64-bit binary string.")
        return

    sign = bits[0]
    eleven_bits = bits[1:12]
    fiftytwo_bits = bits[12:]

    print(f"Sign Bit:    {sign}")
    print(f"11 Bits:    {eleven_bits} ")
    print(f"52 Bits:    {fiftytwo_bits}")
    print(f"Full 64-Bit Binary: {bits}")


def compare_conversions(real_to_float64, float64_to_real, nums, title="Test" , rounding=False):
    """
    Helper function to run conversions and show results for a list of test numbers.
    
    Input:
    real_to_float64_fn (function): a function that takes in a number and an boolean argument
    round that dicates whether to round (True) or chop (False)
    
    float64_to_real_fn (function): a function that takes in a 64-but binary representation
    and converts it to a real number x.
    
    nums (list): a list of test values (float) to compare conversions
    
    title (str): A title for the Tests
    
    round (Boolean): A Boolean indicating whether to round the 64th bit if True
    or chop after the 64th bit if False.
    
    Output: prints results
    
    """
    import math

    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80)
 
    for x in nums:
        bits = real_to_float64(x,rounding)
        recovered = float64_to_real(bits)

        print(f"\nOriginal:  {x}")
        display_components(bits)
        print(f"Recovered: {recovered}")

def compare_methods(real_to_float64, test_val):
    """
    Compare binary outputs from chopping vs rounding.
    
    Input:
    real_to_float64_fn (function): a function that takes in a number and an boolean argument
    round that dicates whether to round (True) or chop (False)
    
    test_val (float): a test value to input in the function above.
    """
    bits_chop = real_to_float64(test_val, round=False)
    bits_round = real_to_float64(test_val, round=True)
    same = bits_chop == bits_round

    print("\n" + "-" * 80)
    print(f"Comparison for {test_val}")
    print("-" * 80)
    print(f"Chopping: {bits_chop}")
    print(f"Rounding: {bits_round}")
    print(f"Same result? {same}")