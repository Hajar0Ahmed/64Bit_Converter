"""
IEEE 754 Conversion Library

A small toolkit for exploring 64-bit floating-point 
(IEEE 754 double precision) representations.

Includes:
- Conversion to binary using chopping and rounding
- Conversion from 64-bit binary to real numbers
- Utilities for displaying and comparing results

Modules:
    converter.py : main conversion functions
    utils.py     : helper tools for display and testing
"""

# __init__.py
from .converter import (
    real_to_float64,
    float64_to_real
)

from .utils import (
    display_components,
    compare_conversions,
    compare_methods
)

__all__ = [
    "real_to_float64",
    "float64_to_real",
    "display_components",
    "compare_conversions",
    "compare_methods",
]
