# Float64 Converter

A Python library and GUI application to convert real numbers to and from **IEEE 754 double-precision (64-bit) binary format**.  

It provides both **chopping** and **rounding** methods.

---

## Features

- Convert **real numbers** to 64-bit IEEE 754 binary strings
- Convert IEEE 754 binary strings back to **real numbers**
- Two conversion styles:
  - **Chopping**: Truncate the mantissa bits
  - **Rounding**: Round to nearest (ties to even)
- Supports **special values** like `0`, `inf`, `-inf`, and `NaN`
- A user-friendly Python GUI application to convert **real numbers** or **mathematical expressions** to **64-bit IEEE 754 binary representation**, and vice versa.  

---
# System Requirements 

`pytest`  (For automated testing of conversion functions and stability testing.)

Make sure Python 3.10+ is installed.

# How to Run the Application:

1. Install the repository

```bash
git clone https://github.com/Hajar0Ahmed/64-Bit_converter
cd float64_converter
```

2. Open terminal
3. Navigate to the project folder:

```bash
cd path/to/64Bit_Converter
```

4. Activate a virtual enviornment

```bash
# For Windows
venv\Scripts\activate

# For macOS/Linux
source venv/bin/activate
```
5. Run the GUI app
```bash
python app.py
```
6. The application window will open. Use it to:

- Enter a real number or mathematical expression (cos(3),e**2,etc.) and convert it to 64-bit binary.
- Enter a 64-bit binary string and convert it back to a real number.
- Copy the binary output using the small Copy button at the bottom right to check conversion both ways.
