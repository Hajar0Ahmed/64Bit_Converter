"""
converter.py

Tools for converting real numbers to and from their IEEE 754
double-precision (64-bit) binary representations.

Includes two conversion styles:
- Chopping 
- Rounding

"""

import math


def real_to_float64_chopping(number):
    """
    Convert real number to 64-bit IEEE 754 using CHOPPING
    
    Input:
        number (float): Real number to convert
    
    Returns:
        str: 64-bit binary string representation
    """
    
    # Special cases
    if number == 0.0:
        return '0' * 64
    if math.isinf(number):
        sign = '0' if number > 0 else '1'
        return sign + '1' * 11 + '0' * 52
    if math.isnan(number):
        return '0' + '1' * 11 + '1' * 52
    
    # Extract sign
    sign = '1' if number < 0 else '0'
    number = abs(number)
    
    # Normalize to get exponent
    exponent = 0
    temp = number
    
    if temp >= 2:
        while temp >= 2:
            temp /= 2
            exponent += 1
    elif temp < 1:
        while temp < 1:
            temp *= 2
            exponent -= 1
            
    
    # Biased exponent (bias = 1023 for double precision)
    biased_exp = exponent + 1023
    
    # Check for overflow/underflow
    if biased_exp >= 2047: # Overflow to infinity
        return sign + '1'*11 + '0'*52
    if biased_exp <= 0:  # Underflow to zero
        return sign + '0'*63
    
    exp_bits = format(biased_exp, '011b')
       
    
    # Extract mantissa (52 bits with chopping)
    mantissa = temp - 1.0  # Remove implicit leading 1
    mantissa_bits = ''
    
    for i in range(52):
        mantissa *= 2
        if mantissa >= 1:
            mantissa_bits += '1'
            mantissa -= 1
        else:
            mantissa_bits += '0'
    
    return sign + exp_bits + mantissa_bits


def real_to_float64_rounding(number):
    """
    Convert real number to 64-bit IEEE 754 using ROUNDING
    
    Input:
        number (float): Real number to convert
    
    Returns:
        str: 64-bit binary string representation
    """
    # Special cases
    if number == 0.0:
        return '0' * 64
    if math.isinf(number):
        return ('0' if number > 0 else '1') + '1'*11 + '0'*52
    if math.isnan(number):
        return '0' + '1'*11 + '1'*52
    
    # Extract sign
    sign = '1' if number < 0 else '0'
    number = abs(number)
    
    # Normalize to get exponent
    exponent = 0
    temp = number
    
    if temp >= 2:
        while temp >= 2:
            temp /= 2
            exponent += 1
    elif temp < 1:
        while temp < 1:
            temp *= 2
            exponent -= 1
    
    # Biased exponent
    biased_exp = exponent + 1023
    
    # Check for overflow/underflow
    if biased_exp >= 2047:
        return sign + '1'*11 + '0'*52
    if biased_exp <= 0:
        return sign + '0'*63
    
    # Extract mantissa (53 bits for rounding decision)
    mantissa = temp - 1.0
    mantissa_bits = ''
    
    for i in range(53):
        mantissa *= 2
        if mantissa >= 1:
            mantissa_bits += '1'
            mantissa -= 1
        else:
            mantissa_bits += '0'
    
    # Apply rounding
    if mantissa_bits[52] == '1':
        # Round up
        mantissa_int = int(mantissa_bits[:52], 2) + 1
        if mantissa_int >= 2**52:
            # Mantissa overflow
            biased_exp += 1
            mantissa_bits = '0' * 52
        else:
            mantissa_bits = format(mantissa_int, '052b')
    else:
        mantissa_bits = mantissa_bits[:52]
    
    exp_bits = format(biased_exp, '011b')
    return sign + exp_bits + mantissa_bits

def float64_to_real(bit_string):
    """
    Convert 64-bit IEEE 754 representation to real number
    
    Input:
        bit_string (str): 64-bit binary string
    
    Returns:
        float: Real number representation
    """
    #Check for valid input
    if len(bit_string) != 64 or any(c not in '01' for c in bit_string):
        raise ValueError("Input must be a 64-bit binary string")
    
    # Extract components
    sign = -1 if bit_string[0] == '1' else 1
    exponent = int(bit_string[1:12], 2)
    mantissa_bits = bit_string[12:]
    
    # Special cases
    if exponent == 2047:  # All 1s in exponent
        if mantissa_bits == '0' * 52:
            return sign * float('inf')
        else:
            return float('nan')
    
    if exponent == 0:  # Zero or denormalized
        if mantissa_bits == '0' * 52:
            return 0.0
        else:
            # Denormalized number
            mantissa_value = 0.0
            for i, bit in enumerate(mantissa_bits):
                if bit == '1':
                    mantissa_value += 2 ** (-(i + 1))
            return sign * mantissa_value * (2 ** -1022)
    
    # Normalized number
    mantissa_value = 1.0  # Implicit leading 1
    for i, bit in enumerate(mantissa_bits):
        if bit == '1':
            mantissa_value += 2 ** (-(i + 1))
    
    # Calculate final value
    real_exponent = exponent - 1023
    result = sign * mantissa_value * (2 ** real_exponent)
    
    return result