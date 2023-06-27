import math
import tkinter as tk
from tkinter import messagebox

# Стандартні розміри листів металу
standard_sizes = [
    {'length': 2500, 'width': 1250},
    {'length': 2000, 'width': 1000}
    # Додайте інші стандартні розміри, якщо потрібно
]

def calculate_optimal_cuts():
    try:
        gate_width = int(width_entry.get())
        gate_height = int(height_entry.get())

        total_area = gate_width * gate_height
        optimal_layout = None
        min_waste = float('inf')

        # Проходимося по всім комбінаціям стандартних розмірів
        for size in standard_sizes:
            layout = get_layout(gate_width, gate_height, size['length'], size['width'])
            waste = size['length'] * size['width'] * layout['unused']

            # Знаходимо найменшу кількість відходів
            if waste < min_waste:
                min_waste = waste
                optimal_layout = layout

        show_results(optimal_layout)
    except ValueError:
        messagebox.showerror("Помилка", "Будь ласка, введіть числові значення для ширини та висоти.")

def get_layout(gate_width, gate_height, sheet_length, sheet_width):
    # Розміри воріт
    width_cuts = math.ceil(gate_width / sheet_width)
    height_cuts = math.ceil(gate_height / sheet_length)

    # Розміщення на аркуші
    sheet_layout = {
        'width': sheet_width,
        'length': sheet_length,
        'count': width_cuts * height_cuts,
        'unused': (width_cuts * sheet_width * height_cuts * sheet_length - gate_width * gate_height) / (sheet_width * sheet_length)
    }

    return sheet_layout

def show_results(layout):
    result_text = f"Кількість листів: {layout['count']}\n\nРозміщення на листах:\nШирина\tДовжина\tКількість\n"
    result_text += f"{layout['width']}\t{layout['length']}\t{layout['count']}"
    result_label.configure(text=result_text)

# Створення головного вікна
window = tk.Tk()
window.title("Розрахунок розміщення листів металу")

# Елементи управління
width_label = tk.Label(window, text="Ширина воріт (мм):")
width_label.pack()
width_entry = tk.Entry(window)
width_entry.pack()

height_label = tk.Label(window, text="Висота воріт (мм):")
height_label.pack()
height_entry = tk.Entry(window)
height_entry.pack()

calculate_button = tk.Button(window, text="Розрахувати", command=calculate_optimal_cuts)
calculate_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

# Запуск головного циклу програми
window.mainloop()


# pip install tk
