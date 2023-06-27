import tkinter as tk
from tkinter import messagebox

def calculate_optimal_cuts():
    gate_width = int(width_entry.get())
    gate_height = int(height_entry.get())

    # Стандартні розміри листів металу
    standard_sizes = [
        {'length': 2500, 'width': 1250},
        {'length': 2000, 'width': 1000}
        # Додайте інші стандартні розміри, якщо потрібно
    ]

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

    cut_pieces = get_cut_pieces(optimal_layout, gate_width, gate_height)
    piece_counts = count_cut_pieces(cut_pieces)
    show_results(optimal_layout, cut_pieces, piece_counts)

def get_layout(gate_width, gate_height, sheet_length, sheet_width):
    # Розміри воріт
    width_cuts = -(-gate_width // sheet_width)
    height_cuts = -(-gate_height // sheet_length)

    # Розміщення на аркуші
    sheet_layout = {
        'width': sheet_width,
        'length': sheet_length,
        'count': width_cuts * height_cuts,
        'unused': (width_cuts * sheet_width * height_cuts * sheet_length - gate_width * gate_height) / (sheet_width * sheet_length)
    }

    return sheet_layout

def get_cut_pieces(layout, gate_width, gate_height):
    cut_pieces = []

    piece_width = gate_width % layout['width']
    if piece_width > 0:
        piece_height = layout['length']
        cut_pieces.append({'width': piece_width, 'height': piece_height})

    piece_height = gate_height % layout['length']
    if piece_height > 0:
        piece_width = layout['width']
        cut_pieces.append({'width': piece_width, 'height': piece_height})

    return cut_pieces

def count_cut_pieces(cut_pieces):
    piece_counts = {}

    for piece in cut_pieces:
        key = f"{piece['width']}x{piece['height']}"

        if key in piece_counts:
            piece_counts[key] += 1
        else:
            piece_counts[key] = 1

    return piece_counts

def show_results(layout, cut_pieces, piece_counts):
    result_text = f"Кількість листів: {layout['count']}\n\nРозміщення на листах:\nШирина\tДовжина\tКількість\n"
    result_text += f"{layout['width']}\t{layout['length']}\t{layout['count']}"

    if cut_pieces:
        result_text += "\n\nПорізані кусочки:\nШирина\tДовжина\tКількість\n"
        for piece in cut_pieces:
            key = f"{piece['width']}x{piece['height']}"
            result_text += f"{piece['width']}\t{piece['height']}\t{piece_counts[key]}\n"

    messagebox.showinfo("Результати", result_text)

# Створення вікна
window = tk.Tk()
window.title("Розрахунок розміщення листів металу та порізка кусочків")

# Елементи інтерфейсу
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

# Запуск головного циклу програми
window.mainloop()
