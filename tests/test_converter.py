"""
tests/test_converter.py

Contains Automated pytest tests that test:
1. Basic Functionality of the Algorithms
2. Edge Cases
4. Rounding and Chopping
5. Stability and Error
"""

import os, sys, math
import pytest
from decimal import Decimal

# Find package
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from float64_converter.converter import real_to_float64, float64_to_real

# Machine Epsilon for 64-bit float: 2^-52
MACHINE_EPSILON = Decimal(2)**Decimal(-52)

# Theoretical bounds for relative error:
# 1. Tighter bound for correct rounding (Round Half to Even)
ROUNDING_BOUND = MACHINE_EPSILON / 2 
# 2. Looser bound for chopping (Maximum error is 1 ulp)
CHOPPING_BOUND = MACHINE_EPSILON 



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

        
        

STABILITY_TEST_VALUES = [
    Decimal("0"),
    Decimal("-0"),
    Decimal("1"),
    Decimal("-1"),
    Decimal("3.141592653589793"),
    Decimal("2.718281828459045"),
    Decimal("1E-308"),  #denormalized range
    Decimal("1E-300"),
    Decimal("1E+300"),
]

@pytest.mark.parametrize("x", STABILITY_TEST_VALUES)
@pytest.mark.parametrize("rounding", [True, False])
def test_stability_and_error(x, rounding):
    """
    Test that:
    1. Converting to 64-bit float and back stays within the theoretical relative error bound (Error Analysis)
    2. Small perturbations in input do not cause disproportionate changes in output (Stability Analysis)
    """
    try:
        bits = real_to_float64(x, round=rounding)
        x_comp = float64_to_real(bits)
    except InvalidOperation:
        pytest.fail(f"Decimal operation failed for x={x}, rounding={rounding}")

    # Skip special values
    if isinstance(x_comp, float) and (math.isnan(x_comp) or math.isinf(x_comp)):
        pytest.skip("Skipping special value test (NaN or Infinity)")

    # Convert to Decimal for precise error calculation
    x_true_dec = Decimal(str(x))
    x_comp_dec = Decimal(str(x_comp))

    # 1. Error Analysis
    abs_error = abs(x_true_dec - x_comp_dec)
    rel_error = Decimal(0) if x_true_dec.is_zero() else abs_error / abs(x_true_dec)

    current_bound = ROUNDING_BOUND if rounding else CHOPPING_BOUND
    mode_name = 'Rounding (Epsilon/2)' if rounding else 'Chopping (Epsilon)'

    # Skip denomalized numbers
    if abs(x_true_dec) >= Decimal(2) ** -1022:
        assert rel_error <= current_bound, (
            f"Relative error {rel_error} exceeded bound for x={x} in {mode_name} mode. "
            f"Bound: {current_bound}"
        )
 
    # 2. Stability Analysis
    
    # Small variation in input
    delta = Decimal('1e-15') * max(Decimal(1), abs(x_true_dec))
    x_plus = x_true_dec + delta
    x_minus = x_true_dec - delta

    # Convert values
    comp_plus = Decimal(str(float64_to_real(real_to_float64(x_plus, round=rounding))))
    comp_minus = Decimal(str(float64_to_real(real_to_float64(x_minus, round=rounding))))

    # Numerical sensitivity (approx derivative)
    sensitivity = abs(comp_plus - comp_minus) / (2 * delta)

    # Stability criterion: output should not be disproportionately large
    # Typically, for IEEE 64-bit floats, sensitivity <= 1 is expected for well-behaved numbers
    # (We can allow a tiny margin due to rounding)
    assert sensitivity <= Decimal(1.1), (
        f"Sensitivity {sensitivity} too high for x={x} in {mode_name} mode"
    )