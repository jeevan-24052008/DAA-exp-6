import tkinter as tk
from tkinter import messagebox


def matrix_chain_order(dimensions):
    """Find the minimum scalar multiplications using dynamic programming."""
    matrix_count = len(dimensions) - 1
    costs = [[0] * (matrix_count + 1) for _ in range(matrix_count + 1)]
    splits = [[0] * (matrix_count + 1) for _ in range(matrix_count + 1)]

    for chain_length in range(2, matrix_count + 1):
        for start in range(1, matrix_count - chain_length + 2):
            end = start + chain_length - 1
            costs[start][end] = float("inf")

            for split in range(start, end):
                cost = (
                    costs[start][split]
                    + costs[split + 1][end]
                    + dimensions[start - 1] * dimensions[split] * dimensions[end]
                )
                if cost < costs[start][end]:
                    costs[start][end] = cost
                    splits[start][end] = split
    return costs, splits


def optimal_order(splits, start, end):
    if start == end:
        return f"A{start}"
    split = splits[start][end]
    return f"({optimal_order(splits, start, split)} x {optimal_order(splits, split + 1, end)})"


def create_cost_table(costs, matrix_count):
    lines = ["DP Cost Table", ""]
    header = "       " + "".join(f"A{column:<10}" for column in range(1, matrix_count + 1))
    lines.append(header)

    for row in range(1, matrix_count + 1):
        line = f"A{row:<5}"
        for column in range(1, matrix_count + 1):
            value = "---" if column < row else str(costs[row][column])
            line += f"{value:<12}"
        lines.append(line)
    return "\n".join(lines)


def calculate_order():
    try:
        dimensions = [int(value.strip()) for value in dimensions_entry.get().split(",")]
        if len(dimensions) < 2 or any(value <= 0 for value in dimensions):
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid input", "Enter at least two positive dimensions separated by commas.")
        return

    matrix_count = len(dimensions) - 1
    costs, splits = matrix_chain_order(dimensions)
    matrix_sizes = ", ".join(
        f"A{index + 1} ({dimensions[index]} x {dimensions[index + 1]})"
        for index in range(matrix_count)
    )

    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.insert(
        tk.END,
        f"Matrices: {matrix_sizes}\n\n"
        f"Minimum scalar multiplications: {costs[1][matrix_count]}\n"
        f"Optimal parenthesization: {optimal_order(splits, 1, matrix_count)}\n\n"
        f"{create_cost_table(costs, matrix_count)}",
    )
    result_text.config(state="disabled")


root = tk.Tk()
root.title("Matrix Chain Multiplication")
root.geometry("800x560")

tk.Label(root, text="Matrix Chain Multiplication", font=("Arial", 16, "bold")).pack(pady=(18, 12))
tk.Label(root, text="Enter dimensions separated by commas:").pack()
tk.Label(root, text="Example: 10, 30, 5, 60, 10  creates A1(10×30), A2(30×5), ...").pack(pady=(2, 5))

dimensions_entry = tk.Entry(root, width=55)
dimensions_entry.pack(pady=5)
dimensions_entry.insert(0, "10, 30, 5, 60, 10")

tk.Button(root, text="Calculate Optimal Order", command=calculate_order, width=23).pack(pady=13)

result_text = tk.Text(root, height=20, width=92, state="disabled", font=("Consolas", 10))
result_text.pack(padx=15, pady=(0, 15))

root.mainloop()