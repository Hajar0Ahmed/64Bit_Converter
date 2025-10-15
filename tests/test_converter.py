"""
tests/test_converter.py

Contains:
1. Demo runs (for interactive testing)
2. Automated pytest tests (for correctness checking)
"""

import os, sys, math
import pytest

# Find package
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from float64_converter.converter import real_to_float64, float64_to_real
from float64_converter.utils import compare_conversions, compare_methods


# Pytest 
def test_basic():
    """
    Test that converts a number to it's 64 bit binary representation
    and back gives approximately the same value.
    
    """
    values = [0.0, 1.0, -1.0, 12.375, -12.375, 0.1, 
              math.sqrt(2),1.0 + 2**30,1.5 + 2**-50, 123456789.123456789]
    for val in values:
        chopped_bits = real_to_float64(val, round=False)
        rounded_bits = real_to_float64(val, round=True)        

        # Verify that if you convert it to 64bits and back to a number it is the same
        chopped_value = float64_to_real(chopped_bits)
        rounded_value = float64_to_real(rounded_bits)
        assert math.isclose(val, chopped_value, rel_tol=1e-15, abs_tol=1e-15)
        assert math.isclose(val, rounded_value, rel_tol=1e-15, abs_tol=1e-15)

def test_special_values():
    """Check handling of special IEEE 754 values."""
    # Positive infinity
    inf_val = float("inf")
    inf_bits = real_to_float64(inf_val)
    assert float64_to_real(inf_bits) == inf_val
    assert len(inf_bits) == 64
    
    # Negative infinity
    neg_inf_val = float("-inf")
    neg_inf_bits = real_to_float64(neg_inf_val)
    assert float64_to_real(neg_inf_bits) == neg_inf_val
    assert len(neg_inf_bits) == 64
    
    # NaN
    nan_val = float("nan")
    nan_bits = real_to_float64(nan_val)
    recon_nan = float64_to_real(nan_bits)
    assert math.isnan(recon_nan)
    assert len(nan_bits) == 64


