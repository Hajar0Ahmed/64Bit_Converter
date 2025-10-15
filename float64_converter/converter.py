"""
converter.py

Tools for converting real numbers to and from their IEEE 754
double-precision (64-bit) binary representations.

Includes two conversion styles:
- Chopping 
- Rounding

"""

import math

def real_to_float64(x , round=False):
    """
    Convert real number to 64-bit IEEE 754 using the formula:
    
     x =  (-1)^s * 2^(c-1023) * (f+1)
    
    Input:
        x (float): Real number to convert
        
        round (boolean): A Boolean indicating whether to round the 64th bit if True
        or chop after the 64th bit if False.
    
    Returns:
        str: 64-bit binary string representation
    """
    # Step 1: Find s
    s = 0 if x >= 0 else 1
    x = abs(x)
    
    # Check for The Following Special Cases
    if math.isnan(x):
        # x is undefined or something we can't calculate
        return "0" + "1" * 11 + "1" + "0" * 51  # NaN
    if math.isinf(x):
        # x is infinity or negative infinity
        return f"{s}" + "1" * 11 + "0" * 52
    if x == 0.0:
        # x is zero
        return f"{s}" + "0" * 63
    
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
    
    # Step 3: Find 11bit: c10,c9,c8,...,c0
    eleven_bits = format(c, '011b')
    
    # Step 4: Find 52bit: f1,f2,...,f53 (extra bit for rounding)
    fiftythree_bits = ''
    ftemp = f
    
    for _ in range(53):
        # f = f1*2^-1 + f2*2^-2 + ... + f52*2^-52 + f53*2^-53
        ftemp *= 2
        bit = int(ftemp)
        fiftythree_bits += str(bit)
        ftemp -= bit
    
    # Step 5: Chopping result
    fiftytwo_bits = fiftythree_bits[:52]
    
    # Step 6: Rounding
    if round:
        # store the fifty third bit
        f52 = fiftythree_bits[52]
        # check if we need to round
        if f52 == '1':
            # find f_int with f = 0.f_int then round up by adding 1
            f_int = int(fiftytwo_bits, 2) + 1
            # convert it back to 52-bits
            fiftytwo_bits = format(f_int, '052b')
            
            # Handle overflow into cpart
            if len(fiftytwo_bits) > 52:
                fiftytwo_bits = fiftytwo_bits[-52:]
                cpart = int(eleven_bits, 2) + 1
                eleven_bits = format(cpart, '011b')
    
    return f"{s}" + eleven_bits + fiftytwo_bits
    

def float64_to_real(sixtyfour_bits):
    """
    Convert 64-bit IEEE 754 representation to real number x using the formula:
    
     x =  (-1)^s * 2^(c-1023) * (f+1)
    
    Input:
        sixtyfour_bits (str): 64-bit binary string
    
    Returns:
        x (float): Real number representation
    """
    # Check for valid input
    if len(sixtyfour_bits) != 64 or any(c not in '01' for c in sixtyfour_bits):
        raise ValueError("Input must be a 64-bit binary string")
    
    # Extract components (s,11bit,52bit)
    s = int(sixtyfour_bits[0],2)
    eleven_bits = sixtyfour_bits[1:12]
    fiftytwo_bits = sixtyfour_bits[12:]
    
    # Compute the sign (-1)^s
    sign = (-1) ** s
    
    # Find c
    c = int(eleven_bits, 2)
    
    # Calculate the exponent of 2, (c-1023)
    exponent = c - 1023
    
    # Find f
    fpart = 1.0  
    for i, bit in enumerate(fiftytwo_bits):
        fpart += int(bit) * (2 ** -(i + 1))
    
    # Check special cases
    if eleven_bits == '1'*11:  # all 1s
        if '1' in fiftytwo_bits: # NaN
            return float('nan')
        else: # Positive or Negative Infinity
            return float('inf') if s == 0 else float('-inf')
    elif eleven_bits == '0'*11:  # all 0s
        # case where x=0
        if fiftytwo_bits == '0'*52: 
            return 0.0
        
        # case where x<0
        fpart = 0
        for i, bit in enumerate(fiftytwo_bits):
            fpart += int(bit) * (2 ** -(i + 1))
        return sign * fpart * (2 ** (exponent + 1))

    # Calculate x
    x = sign * fpart * (2 ** exponent)
    return x
