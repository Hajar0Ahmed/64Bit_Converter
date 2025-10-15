import tkinter as tk
from tkinter import ttk
from float64_converter import converter

class IEEE754ConverterApp:
    """
    A GUI application for converting real numbers to and from
    64-bit IEEE 754 floating-point representation.

    Features:
    - Input a real number.
    - Choose conversion method: Chopping or Rounding.
    - Display the 64-bit binary representation and recovered value.
    """

    def __init__(self, root):
        """
        Initialize the application with the main window and widgets.

        Parameters:
            root (tk.Tk): The main Tkinter window.
        """
        self.root = root
        self.root.title("64-bit IEEE 754 Converter")
        self.root.geometry("750x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#1c1c1c")  # Dark gray background

        # StringVar to store user choice of conversion method
        self.method_var = tk.StringVar(value="chop")

        # StringVar to store output text
        self.output_text = tk.StringVar()

        # Create all GUI components
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange all widgets in the application."""
        self._create_header()
        self._create_input_frame()
        self._create_output_frame()
        self._create_footer()

    def _create_header(self):
        """Create the header label at the top of the window."""
        header_label = tk.Label(
            self.root,
            text="64-bit IEEE 754 Converter",
            font=("Segoe UI", 22, "bold"),
            bg="#1c1c1c",
            fg="#e0e0e0"
        )
        header_label.pack(pady=15)

    def _create_input_frame(self):
        """Create the input frame containing entry, radio buttons, and convert button."""
        frame = tk.Frame(self.root, bg="#2c2c2c")
        frame.pack(pady=10, fill="x", padx=20)

        # Label for entry
        tk.Label(
            frame,
            text="Enter a real number:",
            font=("Segoe UI", 12),
            bg="#2c2c2c",
            fg="#ffffff"
        ).pack(side="left", padx=(0, 10))

        # Entry widget for user input
        self.entry = tk.Entry(
            frame,
            font=("Consolas", 12),
            width=20,
            bg="#3a3a3a",
            fg="#ffffff",
            insertbackground="white",
            relief="flat"
        )
        self.entry.pack(side="left")

        # Frame for radio buttons
        radio_frame = tk.Frame(frame, bg="#2c2c2c")
        radio_frame.pack(side="left", padx=15)

        # Create radio buttons
        self._create_radio_button(radio_frame, "Chopping", "chop", "#cccccc")
        self._create_radio_button(radio_frame, "Rounding", "round", "#aaaaaa")

        # Convert button
        tk.Button(
            frame,
            text="Convert",
            command=self.convert_number,
            font=("Segoe UI", 12, "bold"),
            bg="#555555",
            fg="#ffffff",
            activebackground="#777777",
            activeforeground="#ffffff",
            relief="flat",
            padx=10,
            pady=5
        ).pack(side="left", padx=10)

    def _create_radio_button(self, parent, text, value, fg_color):
        """
        Create a single radio button.

        Parameters:
            parent (tk.Widget): Parent container for the radio button.
            text (str): Label for the radio button.
            value (str): Value assigned when the button is selected.
            fg_color (str): Text color for the radio button.
        """
        tk.Radiobutton(
            parent,
            text=text,
            variable=self.method_var,
            value=value,
            font=("Segoe UI", 11),
            bg="#2c2c2c",
            fg=fg_color,
            selectcolor="#3a3a3a",
            activeforeground=fg_color,
            activebackground="#2c2c2c"
        ).pack(side="top", anchor="w")

    def _create_output_frame(self):
        """Create the output area to display results."""
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

    def _create_footer(self):
        """Create the footer label at the bottom of the window."""
        footer_label = tk.Label(
            self.root,
            text="Python 64-bit IEEE 754 Converter",
            font=("Segoe UI", 10),
            bg="#1c1c1c",
            fg="#888888"
        )
        footer_label.pack(side="bottom", pady=10)

    def convert_number(self):
        """
        Convert the input number to 64-bit IEEE 754 format based on
        the selected method and display the results.
        """
        try:
            # Read user input
            number = float(self.entry.get())
            method = self.method_var.get()

            # Perform conversion based on method
            if method == "chop":
                binary_repr = converter.real_to_float64(number)
            else:
                binary_repr = converter.real_to_float64(number, round=True)

            # Recover the real number from binary
            recovered_value = converter.float64_to_real(binary_repr)

            # Update output text
            self.output_text.set(f"Binary: {binary_repr}\nRecovered: {recovered_value}")

        except ValueError:
            self.output_text.set("Invalid input! Please enter a valid number.")


if __name__ == "__main__":
    root = tk.Tk()
    app = IEEE754ConverterApp(root)
    root.mainloop()
