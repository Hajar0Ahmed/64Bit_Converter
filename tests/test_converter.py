"""
test_converter.py

Basic tests and demos for the IEEE 754 converter library.
Run this file directly to verify correctness of the chopping
and rounding implementations.
"""

import math
from converter import (
    real_to_float64_chopping,
    real_to_float64_rounding,
    float64_to_real
)
from utils import display_components, compare_conversions, compare_methods


if __name__ == "__main__":
    # A few values that test special cases, positives, and negatives
    test_values = [
        0.0, 1.0, -1.0,
        12.375, -12.375,
        0.1, 1.875 * (2 ** 10),
        float("inf"), float("-inf"), float("nan")
    ]

    # --- Test chopping ---
    compare_conversions(
        real_to_float64_chopping,
        float64_to_real,
        test_values,
        title="CHOPPING METHOD"
    )

    # --- Test rounding ---
    compare_conversions(
        real_to_float64_rounding,
        float64_to_real,
        test_values,
        title="ROUNDING METHOD"
    )

    # Direct comparison example
    compare_methods(
        real_to_float64_chopping,
        real_to_float64_rounding,
        test_val=12.375
    )

    #sanity check
    print("\nManual check:")
    x = 0.15625
    bits = real_to_float64_rounding(x)
    print(f"\nNumber: {x}")
    display_components(bits)
    print("Recovered:", float64_to_real(bits))