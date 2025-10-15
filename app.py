import tkinter as tk
from tkinter import ttk
from float64_converter import converter
import math
import numpy as np

class IEEE754ConverterApp:
    """
    A GUI application for converting expressions to 64-bit IEEE 754
    floating-point representation and vice versa.

    Features:
    - Input a real number or a mathematical expression (e.g., sin(2), sqrt(5), e^3, 1+29*e).
    - Input a 64-bit binary string to convert back to a real number.
    - Choose conversion method: Chopping or Rounding.
    - Copy the output to clipboard.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("64-bit IEEE 754 Converter")
        self.root.state('zoomed')  # Fullscreen
        self.root.configure(bg="#1c1c1c")  # Dark gray background

        # Variables
        self.method_var = tk.StringVar(value="chop")
        self.output_text = tk.StringVar()
        self.input_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="expression")  # Expression or Binary

        self.create_widgets()

    def create_widgets(self):
        self._create_header()
        self._create_instructions()
        self._create_mode_frame()
        self._create_input_frame()
        self._create_output_frame()
        self._create_footer()

    def _create_header(self):
        tk.Label(
            self.root,
            text="64-bit IEEE 754 Converter",
            font=("Segoe UI", 24, "bold"),
            bg="#1c1c1c",
            fg="#e0e0e0"
        ).pack(pady=15)

    def _create_instructions(self):
        frame = tk.LabelFrame(
            self.root,
            text="Instructions",
            font=("Segoe UI", 14, "bold"),
            bg="#2c2c2c",
            fg="#ffffff",
            bd=2,
            relief="ridge",
            labelanchor="n",
            padx=10,
            pady=10
        )
        frame.pack(pady=10, fill="x", padx=20)

        instruction_text = (
            "• Enter a mathematical expression (e.g., sin(2), sqrt(5), e^3, 1+29*e) and convert it to 64-bit binary.\n"
            "• Or enter a 64-bit binary string to convert back to a real number.\n"
            "• Choose Chopping or Rounding for expression → binary conversion.\n"
            "• Click Convert to see the result, and Copy to copy the output."
        )

        tk.Label(
            frame,
            text=instruction_text,
            justify="left",
            font=("Segoe UI", 12),
            bg="#2c2c2c",
            fg="#ffffff"
        ).pack(anchor="w")

    def _create_mode_frame(self):
        frame = tk.Frame(self.root, bg="#2c2c2c")
        frame.pack(pady=5, fill="x", padx=20)

        tk.Radiobutton(
            frame,
            text="Expression → Binary",
            variable=self.mode_var,
            value="expression",
            font=("Segoe UI", 11),
            bg="#2c2c2c",
            fg="#cccccc",
            selectcolor="#3a3a3a"
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            frame,
            text="Binary → Real Number",
            variable=self.mode_var,
            value="binary",
            font=("Segoe UI", 11),
            bg="#2c2c2c",
            fg="#cccccc",
            selectcolor="#3a3a3a"
        ).pack(side="left", padx=10)

    def _create_input_frame(self):
        frame = tk.Frame(self.root, bg="#2c2c2c")
        frame.pack(pady=10, fill="x", padx=20)

        tk.Label(
            frame,
            text="Input:",
            font=("Segoe UI", 12),
            bg="#2c2c2c",
            fg="#ffffff"
        ).pack(side="left", padx=(0, 10))

        self.entry = tk.Entry(
            frame,
            font=("Consolas", 12),
            width=40,
            textvariable=self.input_var,
            bg="#3a3a3a",
            fg="#ffffff",
            insertbackground="white",
            relief="flat"
        )
        self.entry.pack(side="left")

        method_frame = tk.Frame(frame, bg="#2c2c2c")
        method_frame.pack(side="left", padx=15)

        tk.Radiobutton(
            method_frame,
            text="Chopping",
            variable=self.method_var,
            value="chop",
            font=("Segoe UI", 11),
            bg="#2c2c2c",
            fg="#cccccc",
            selectcolor="#3a3a3a"
        ).pack(anchor="w")
        tk.Radiobutton(
            method_frame,
            text="Rounding",
            variable=self.method_var,
            value="round",
            font=("Segoe UI", 11),
            bg="#2c2c2c",
            fg="#aaaaaa",
            selectcolor="#3a3a3a"
        ).pack(anchor="w")

        tk.Button(
            frame,
            text="Convert",
            command=self.convert,
            font=("Segoe UI", 12, "bold"),
            bg="#555555",
            fg="#ffffff",
            activebackground="#777777",
            relief="flat",
            padx=10,
            pady=5
        ).pack(side="left", padx=10)

    def _create_output_frame(self):
        frame = tk.LabelFrame(
            self.root,
            text="Result",
            font=("Segoe UI", 14, "bold"),
            bg="#3a3a3a",
            fg="#e0e0e0",
            bd=2,
            relief="ridge",
            labelanchor="n",
            padx=10,
            pady=10
        )
        frame.pack(pady=20, fill="both", expand=True, padx=20)

        tk.Label(
            frame,
            textvariable=self.output_text,
            justify="left",
            font=("Consolas", 12),
            bg="#3a3a3a",
            fg="#ffffff"
        ).pack(anchor="w")

        # Copy button at bottom right
        tk.Button(
            frame,
            text="Copy",
            command=self.copy_output,
            font=("Segoe UI", 10),
            bg="#555555",
            fg="#ffffff",
            activebackground="#777777",
            relief="flat",
            padx=5,
            pady=2
        ).pack(anchor="e", side="bottom", pady=5)

    def _create_footer(self):
        tk.Label(
            self.root,
            text="Python 64-bit IEEE 754 Converter",
            font=("Segoe UI", 10),
            bg="#1c1c1c",
            fg="#888888"
        ).pack(side="bottom", pady=10)

    def convert(self):
        mode = self.mode_var.get()
        user_input = self.input_var.get().strip()

        try:
            if mode == "expression":
                # Evaluate expression safely
                allowed_names = {
                    k: getattr(math, k) for k in dir(math) if not k.startswith("__")
                }
                allowed_names.update({"e": math.e, "pi": math.pi})
                number = eval(user_input, {"__builtins__": None}, allowed_names)
                method = self.method_var.get()
                if method == "chop":
                    binary_repr = converter.real_to_float64(number)
                else:
                    binary_repr = converter.real_to_float64(number, round=True)
                self.output_text.set(f"{binary_repr}")
            else:
                # Binary → Real
                if len(user_input) != 64 or any(c not in "01" for c in user_input):
                    raise ValueError("Input must be a 64-bit binary string")
                real_val = converter.float64_to_real(user_input)
                self.output_text.set(f"{real_val}")

        except Exception as e:
            self.output_text.set(f"Error: {str(e)}")

    def copy_output(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = IEEE754ConverterApp(root)
    root.mainloop()
