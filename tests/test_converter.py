"""
tests/test_converter.py

Contains:
1. Demo runs (for interactive testing)
2. Automated pytest tests (for correctness checking)
"""

import os, sys, math
import pytest
from decimal import Decimal

# Find package
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from float64_converter.converter import real_to_float64, float64_to_real

def test_basic():
    """
    Test that converts a number to it's 64 bit binary representation
    and gives back approximately the same value.
    
    """
    values = [# 1. Exact Binary Representation (should recover perfectly)
        0.0, -0.0, 12.375, -12.375, 
        
        # 2. Standard Approximation (non-terminating binary)
        math.sqrt(2), 0.1,
        
        # 3. Very big and very small
        1.0 + 2**30, # Large number to test positive exponent range
        2**-50, # Small number to test negative exponent range
        
        # 4. Values near machine epsilon
        1.0 + 2**-52, # Smallest representable increment (machine epsilon)
        ]
    
    for val in values:
        # Note: These values rely on Decimal.from_float(val) to be accurate for Python floats.
        chopped_bits = real_to_float64(val, round=False)
        rounded_bits = real_to_float64(val, round=True)        

        # Verify that if you convert it to 64bits and back to a number it is the same
        chopped_value = float64_to_real(chopped_bits)
        rounded_value = float64_to_real(rounded_bits)
        assert math.isclose(val, chopped_value, rel_tol=1e-15, abs_tol=1e-15)
        assert math.isclose(val, rounded_value, rel_tol=1e-15, abs_tol=1e-15)

def test_special_values():
    """Tests edge cases"""
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

def test_chopping_vs_rounding():
    """
    Compare rounding vs chopping for a set of representative numbers.
    - Includes a test case that guarantees to produce different bit strings.
    - Ensures rounding is at least as accurate as chopping.
    """
    
    # A value that is different when you chop and round
    val = Decimal('1') + Decimal(2)**-51 + Decimal(2)**-54

    chop_bits = real_to_float64(val, round=False)
    round_bits = real_to_float64(val, round=True)
    
    # Convert back to floats
    chop_val = float64_to_real(chop_bits)
    round_val = float64_to_real(round_bits)

    # Compute relative errors (convert val to float for math)
    val_float = float(val)
    
    # Calculate error for chopping
    rel_error_chop = abs(val - chop_val) / abs(val) if val != Decimal(0) else abs(val - chop_val)
    
    # Calculate error for rounding
    rel_error_round = abs(val - round_val) / abs(val) if val != Decimal(0) else abs(val - round_val)

    print(f"Value: {val}, Chopping Error: {rel_error_chop:e}, Rounding Error: {rel_error_round:e}")

    # Rounding should not be worse than chopping
    assert rel_error_round <= rel_error_chop + Decimal(1e-18)  # tiny tolerance for edge cases




def test_64bit_strings():
    # Numbers that are exactly representable in binary
    exact_numbers = [
        "0.5", "1.0", "2.0", "4.0", "20.0", "-20.0"
    ]
    
    for x in exact_numbers:
        chop_bits = real_to_float64(x, round=False)
        round_bits = real_to_float64(x, round=True)
        
        # These should be identical since they are exactly representable
        assert chop_bits == round_bits, f"{x} differs between chop and round"
    
    # Numbers that are not exactly representable in binary
    approx_numbers = [
        "0.1","12345.6789"
    ]
    
    for x in approx_numbers:
        chop_bits = real_to_float64(x, round=False)
        round_bits = real_to_float64(x, round=True)
        
        # These should differ at least in some bit(s)
        assert chop_bits != round_bits, f"{x} unexpectedly identical for chop and round"

    # Optional: Print results for visual inspection
    for x in approx_numbers:
        print(f"{x}: chop={real_to_float64(x, round=False)} round={real_to_float64(x, round=True)}")