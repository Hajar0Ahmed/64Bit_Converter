"""
utils.py

Helper functions for displaying and testing IEEE 754 
64-bit floating point representations.
"""

def display_components(bits):
    """
    Print the sign, exponent, and mantissa from a 64-bit binary string.
    """
    if len(bits) != 64 or any(b not in "01" for b in bits):
        print("Error: Input must be a 64-bit binary string.")
        return

    sign = bits[0]
    exponent = bits[1:12]
    mantissa = bits[12:]

    print(f"Sign bit:    {sign}")
    print(f"Exponent:    {exponent}  (decimal {int(exponent, 2)})")
    print(f"Mantissa:    {mantissa}")
    print(f"Full binary: {bits}")


def compare_conversions(real_to_float64_fn, float64_to_real_fn, nums, title="Test"):
    """
    Quick helper to run conversions and show results for a list of test numbers.
    """
    import math

    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)

    for x in nums:
        bits = real_to_float64_fn(x)
        recovered = float64_to_real_fn(bits)
        error = abs(x - recovered) if not math.isnan(x) else 0

        print(f"\nOriginal:  {x}")
        display_components(bits)
        print(f"Recovered: {recovered}")
        print(f"Error:     {error}")


def compare_methods(fn_chop, fn_round, test_val):
    """
    Compare binary outputs from chopping vs rounding.
    """
    bits_chop = fn_chop(test_val)
    bits_round = fn_round(test_val)
    same = bits_chop == bits_round

    print("\n" + "-" * 70)
    print(f"Comparison for {test_val}")
    print("-" * 70)
    print(f"Chopping: {bits_chop}")
    print(f"Rounding: {bits_round}")
    print(f"Same result? {same}")