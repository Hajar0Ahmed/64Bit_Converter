"""
test_converter.py

Basic tests and demos for the IEEE 754 converter library.
Run this file directly to verify correctness of the chopping
and rounding implementations.
"""
import sys
import os

# Get the absolute path of the project root (one level up from the tests folder)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add it to sys.path so Python can find your package
sys.path.append(project_root)

from float64_converter.converter import (
    real_to_float64,
    float64_to_real
)

from float64_converter.utils import (
    display_components,
    compare_conversions,
    compare_methods
)


if __name__ == "__main__":
    # A few values that test special cases, positives, and negatives
    test_values = [
        0.0, 1.0, -1.0,
        12.375, -12.375,
        0.1, 1.875 * (2 ** 10),2**(1/2),
        float("inf"), float("-inf"), float("nan")
    ]

    #Test chopping
    compare_conversions(
        real_to_float64,
        float64_to_real,
        test_values,
        title="CHOPPING METHOD",
    )

    #Test rounding
    compare_conversions(
        real_to_float64,
        float64_to_real,
        test_values,
        title="ROUNDING METHOD",
        rounding=True
    )

    # Direct comparison example
    compare_methods(
        real_to_float64,
        test_val=12.375
    )