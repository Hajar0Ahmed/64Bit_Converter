"""
converter.py

Tools for converting real numbers to and from their IEEE 754
double-precision (64-bit) binary representations.

Includes two conversion styles:
- Chopping 
- Rounding

"""

import math


def _normalize(num):
    """
    Return (mantissa, exponent) with mantissa= f+1 and exponenet = c-1023
        so num = mantissa * 2**exponent with 1 ≤ mantissa < 2."""
    exp = 0
    while num >= 2:
        num /= 2
        exp += 1
    while num < 1:
        num *= 2
        exp -= 1
    return num, exp


def real_to_float64_chopping(num):
    """
    Convert a real number to IEEE 754 64-bit binary (using chopping).
    """
    if num == 0.0:
        return "0" * 64
    if math.isinf(num):
        return ("0" if num > 0 else "1") + "1"*11 + "0"*52
    if math.isnan(num):
        return "0" + "1"*11 + "1"*52

    sign = "1" if num < 0 else "0"
    num = abs(num)

    m, e = _normalize(num)
    exp = e + 1023
    if not (0 < exp < 2047):
        return sign + ("1"*11 if exp >= 2047 else "0"*11) + "0"*52

    mant_bits = []
    for _ in range(52):
        m *= 2
        if m >= 1:
            mant_bits.append("1")
            m -= 1
        else:
            mant_bits.append("0")

    return sign + f"{exp:011b}" + "".join(mant_bits)


def real_to_float64_rounding(num):
    """
    Convert a real number to IEEE 754 64-bit binary (round to nearest, ties to even).
    """
    if num == 0.0:
        return "0" * 64
    if math.isinf(num):
        return ("0" if num > 0 else "1") + "1"*11 + "0"*52
    if math.isnan(num):
        return "0" + "1"*11 + "1"*52

    sign = "1" if num < 0 else "0"
    num = abs(num)

    m, e = _normalize(num)
    exp = e + 1023
    if not (0 < exp < 2047):
        return sign + ("1"*11 if exp >= 2047 else "0"*11) + "0"*52

    # Make 53 bits for rounding
    bits = []
    for _ in range(53):
        m *= 2
        if m >= 1:
            bits.append("1")
            m -= 1
        else:
            bits.append("0")

    # Round up if the extra bit is 1
    if bits[52] == "1":
        mant = int("".join(bits[:52]), 2) + 1
        if mant == 2**52:  # overflow
            exp += 1
            mant_bits = "0" * 52
        else:
            mant_bits = f"{mant:052b}"
    else:
        mant_bits = "".join(bits[:52])

    return sign + f"{exp:011b}" + mant_bits


def float64_to_real(bits):
    """
    Convert a 64-bit IEEE 754 binary string back to a float.
    """
    if len(bits) != 64 or any(b not in "01" for b in bits):
        raise ValueError("Input must be a 64-bit binary string.")

    sign = -1 if bits[0] == "1" else 1
    exp = int(bits[1:12], 2)
    mant_bits = bits[12:]

    if exp == 2047:
        return sign * float("inf") if mant_bits == "0"*52 else float("nan")

    if exp == 0:  # denormalized
        m = sum(int(b) * 2**-(i+1) for i, b in enumerate(mant_bits))
        return sign * m * 2**-1022 if m else 0.0

    # normalized
    m = 1 + sum(int(b) * 2**-(i+1) for i, b in enumerate(mant_bits))
    return sign * m * 2**(exp - 1023)