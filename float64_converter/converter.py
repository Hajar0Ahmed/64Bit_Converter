"""
converter.py

Tools for converting real numbers to and from their IEEE 754
double-precision (64-bit) binary representations.

Includes two conversion styles:
- Chopping 
- Rounding

"""

import math
from decimal import Decimal, getcontext, ROUND_DOWN, ROUND_HALF_EVEN

getcontext().prec = 70



def real_to_float64(x , round=False):
    """
    Convert a real number (str, Decimal, or float) to 64-bit IEEE 754 using the formula: 
    using the formula:
    
     x =  (-1)^s * 2^(c-1023) * (f+1)
    
    Input:
        x (str, Decimal, or float): Real number to convert.
        round (boolean): A Boolean indicating whether to round the 64th bit if True
        or chop after the 64th bit if False.
    Returns:
        str: 64-bit binary string representation.
    """
    # 1. Convert input to Decimal for high-precision internal math
    if isinstance(x, str):
        x = Decimal(x)
    elif isinstance(x, (float, int)):
        # Convert float to Decimal using its exact string representation
        # to avoid double rounding errors on input.
        x = Decimal.from_float(x)
    elif isinstance(x, Decimal):
        x = x
    else:
        raise TypeError("Input must be a float, int, str, or Decimal.")
    
    
    # Check for The Following Special Cases
    if x.is_nan():
        # x is undefined or something we can't calculate
        return "0" + "1" * 11 + "1" + "0" * 51  # NaN
    
    if x.is_infinite():
        s = 1 if x.is_signed() else 0
        return f"{s}" + "1"*11 + "0"*52
    if x.is_zero():
        s = 1 if x.is_signed() else 0
        return f"{s}" + "0"*63

    #  Normal numbers: now it's safe to compute sign
    s = 1 if x.is_signed() else 0
    x = x.copy_abs()

    
    # Step 2: Find the c and f
    # We use the following Equation: |x| = 2^cpart * fpart
    # Where cparts = c - 1023 and fpart = f + 1 with 1 < fpart <= 2
    
    cpart = 0
    fpart = x
    
    # If x >= 2 we keep dividing it until we have |x| = 2^cpart * fpart
    # with fpart <= 2
    while fpart >= 2:
        fpart /= 2
        cpart += 1
    
    # If fpart < 1 we make a correction by simplifying |x| = 2^(cpart-1)*2*fpart
    # We repeat this process until 1 < fpart <= 2
    while fpart < 1:
        fpart *= 2
        cpart -= 1
        
    # Calculate c from cpart
    c = cpart + 1023
    
    # Calculate f from fpart
    f = fpart - 1
    
    # Check for Overflow/Underflow (if we do NOT have 0 < c < 2047)
    if c >= 2047: # Overflow to infinity
        return f"{s}" + '1'*11 + '0'*52
    if c <= 0:  # Underflow to zero
        return f"{s}" + '0'*63
    
    if round:
        fiftytwo_int = (f * (2**52)).to_integral_value(rounding=ROUND_HALF_EVEN)
    else:
        fiftytwo_int = (f * (2**52)).to_integral_value(rounding=ROUND_DOWN)
    
    # Calculate f_scaled: This is the normalized fraction f, scaled by 2^52
    f_scaled = f * (2**52) # f * 4503599627370496
    
    # ... Apply rounding ...
    
    if fiftytwo_int >= 2**52:
        # 1. Reset mantissa to zero (52 zeros)
        fiftytwo_int = 0
        
        # 2. Increment the exponent
        c += 1
        
        # 3. Check for Exponent Overflow (Infinity)
        if c >= 2047:
            s = 1 if x.is_signed() else 0 # Use the original sign for infinity
            return f"{s}" + '1'*11 + '0'*52

    fiftytwo_bits = format(int(fiftytwo_int), '052b')
    eleven_bits = format(c, '011b')

    # Step 6: Combine sign, exponent, and fraction into 64-bit string
    return f"{s}" + eleven_bits + fiftytwo_bits


def float64_to_real(sixtyfour_bits):
    """
    Convert 64-bit IEEE 754 representation to real number x using the formula:
    
     x =  (-1)^s * 2^(c-1023) * (f+1)
    
    Input:
        sixtyfour_bits (str): 64-bit binary string
    
    Returns:
        x : Real number representation
    """
    if len(sixtyfour_bits) != 64 or any(c not in '01' for c in sixtyfour_bits):
        raise ValueError("Input must be a 64-bit binary string")
    
    # Extract components
    s = int(sixtyfour_bits[0])
    eleven_bits = sixtyfour_bits[1:12]
    fiftytwo_bits = sixtyfour_bits[12:]
    
    sign = Decimal((-1) ** s)
    c = int(eleven_bits, 2)
    exponent = Decimal(c - 1023)
    
    # Check special cases
    if eleven_bits == '1'*11:  # Infinity or NaN
        if '1' in fiftytwo_bits:
            return float('nan')
        else:
            return float('inf') if s == 0 else float('-inf')

    elif eleven_bits == '0'*11:  # Zero or Denormalized (Subnormal)
        # Case where x=0
        if fiftytwo_bits == '0'*52: 
            return 0.0
        
        # Denormalized case (exponent is fixed at -1022, implicit '1' is '0')
        E_denorm = Decimal(-1022) 
        F_denorm = Decimal(0)
        
        # Calculate the fraction (0.f1 f2...)
        for i, bit in enumerate(fiftytwo_bits):
            F_denorm += Decimal(bit) * (Decimal(2) ** Decimal(-(i + 1)))
        
        # Denorm value = sign * 2^-1022 * (0 + F)
        x = sign * F_denorm * (Decimal(2) ** E_denorm)
        
        # We return the raw Decimal object, which is better for error calculation
        return x 

    # Normalized Case (The vast majority of numbers)
    
    # Calculate fpart (1.f1 f2...): Start with the implicit leading '1'
    fpart = Decimal(1) 
    
    # Calculate the fraction part (f)
    for i, bit in enumerate(fiftytwo_bits):
        # *** KEY FIX: Use Decimal for base, exponent, and multiplier ***
        fpart += Decimal(bit) * (Decimal(2) ** Decimal(-(i + 1)))

    # Calculate x = sign * fpart * 2^exponent
    # ** KEY FIX: Use Decimal for the final multiplication **
    x = sign * fpart * (Decimal(2) ** exponent)
    
    # Return Decimal object for use in your table's error calculation
    return x

