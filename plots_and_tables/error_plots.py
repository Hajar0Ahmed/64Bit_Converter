import os, sys, math
from decimal import Decimal, getcontext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd

# Find package
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from float64_converter.converter import real_to_float64, float64_to_real

getcontext().prec = 70

def chop_vs_round_plot():
    '''
    Plot the Relative Error for Randomly generated values to compare chopping and rounding

    Plot is saved as chop_vs_round_plot.png
    '''
    num_points = 70
    x_linspace = np.linspace(-1, 1, num_points)

    test_values = []
    for x in x_linspace:
        # Use a non-terminating fraction for variety
        base_fraction = Decimal(1)/Decimal(3)
        scaled_value = base_fraction * Decimal(str(x))  # scale fraction
        test_values.append(str(scaled_value))

    # Add a few extra small fractions
    test_values += ["0.1", str(Decimal(1)/Decimal(7)), str(Decimal(1)/Decimal(1000))]
    for log_mag in x_linspace:
        scaled_value = base_fraction * (Decimal(10) ** Decimal(log_mag))
        test_values.append(str(scaled_value))

    # Add some extra non-terminating fractions
    test_values += ["0.1", str(Decimal(1)/Decimal(7))]

    # --- Compute chopped & rounded values and errors ---
    X_values, log10_errors_chop, log10_errors_round = [], [], []

    for x_str in test_values:
        chop_bits = real_to_float64(x_str, round=False)
        round_bits = real_to_float64(x_str, round=True)

    x_back_chop = Decimal(str(float64_to_real(chop_bits)))
    x_back_round = Decimal(str(float64_to_real(round_bits)))
    x_dec = Decimal(x_str)

    # Compute relative errors safely
    rel_err_chop = abs(x_dec - x_back_chop)/abs(x_dec) if x_dec != 0 else abs(x_dec - x_back_chop)
    rel_err_round = abs(x_dec - x_back_round)/abs(x_dec) if x_dec != 0 else abs(x_dec - x_back_round)

    # Skip zero errors to avoid log10(0)
    if rel_err_chop > 0 or rel_err_round > 0:
        X_values.append(float(x_dec))
        log10_errors_chop.append(math.log10(float(rel_err_chop)) if rel_err_chop > 0 else np.nan)
        log10_errors_round.append(math.log10(float(rel_err_round)) if rel_err_round > 0 else np.nan)

    # --- Plot ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 6), dpi=120)

    round_color = "#1f77b4"
    chop_color = "#d62728"
    eps_color = "#2ca02c"

    ax.scatter(X_values, log10_errors_round, color=round_color, label="Rounding", s=50, marker='o', edgecolor='black', linewidth=0.5)
    ax.scatter(X_values, log10_errors_chop, color=chop_color, label="Chopping", s=50, marker='x')

    log10_epsilon = math.log10(np.finfo(float).eps)
    ax.axhline(y=log10_epsilon, color=eps_color, linestyle='--', linewidth=1.5, label=f"$\\log_{{10}}(\\varepsilon)$ ≈ {log10_epsilon:.2f}")

    ax.set_xlabel("Original Value (Decimal)", fontsize=12)
    ax.set_ylabel(r"log$_{10}$(Relative Error)", fontsize=12, labelpad=10)
    ax.set_title("Comparison of Chopping vs Rounding Relative Errors in IEEE 754", fontsize=14, fontweight='bold')

    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.grid(alpha=0.25)
    ax.legend(frameon=True, fontsize=10)

    # change y-axis display
    min_y = min(filter(lambda v: not np.isnan(v), log10_errors_chop + log10_errors_round))
    max_y = max(filter(lambda v: not np.isnan(v), log10_errors_chop + log10_errors_round))
    ax.set_ylim(min_y - 0.5, max_y + 0.5)

    plt.tight_layout()

    # Save as png
    output_path = os.path.join(os.path.dirname(__file__), "chop_vs_round_plot.png")
    plt.savefig(output_path, dpi=150)


def test_val_table():
    """
    Compute IEEE 754 Chopped and Rounded values and their Absolute & Relative errors
    """

    test_values = ["12345.6789","3.1415926535"]

    rows_data = []

    for x_str in test_values:
        x_dec = Decimal(str(eval(x_str)))
        
        # Convert using your functions
        x_chop_bits = real_to_float64(x_dec, round=False)
        x_round_bits = real_to_float64(x_dec, round=True)

        x_chop_val = float64_to_real(x_chop_bits)
        x_round_val = float64_to_real(x_round_bits)

        # Absolute and Relative Errors
        abs_err_chop = abs(x_dec - x_chop_val)
        abs_err_round = abs(x_dec - x_round_val)
        rel_err_chop = abs_err_chop / abs(x_dec) if x_dec != 0 else abs_err_chop
        rel_err_round = abs_err_round / abs(x_dec) if x_dec != 0 else abs_err_round

        rows_data.append({
            "Original Value": x_str,
            "Chopped Value": float(x_chop_val),
            "Rounded Value": float(x_round_val),
            "Abs. Error (Chop)": float(abs_err_chop),
            "Rel. Error (Chop)": float(rel_err_chop),
            "Abs. Error (Round)": float(abs_err_round),
            "Rel. Error (Round)": float(rel_err_round),
        })

    df = pd.DataFrame(rows_data)

    # Optional: format numeric columns nicely for display
    df_display = df.copy()
    numeric_cols = df.columns[1:]
    df_display[numeric_cols] = df_display[numeric_cols].applymap(lambda x: f"{x:.2e}" if abs(x) < 1e3 else f"{x:.17g}")

    # Export LaTeX code
    latex_code = df_display.to_latex(index=False, escape=False, column_format='lrrrrrr',
                                     caption="IEEE 754 Conversion Results: Chopped vs. Rounded Values",
                                     label="tab:ieee754_results")
    with open("ieee754_table.tex", "w") as f:
        f.write(latex_code)
    
    return latex_code

if __name__=="__main__":
    chop_vs_round_plot()
    test_val_table()
    