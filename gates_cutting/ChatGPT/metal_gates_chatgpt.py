import math

# Стандартні розміри листів металу
standard_sizes = [
    {'length': 2500, 'width': 1250},
    {'length': 2000, 'width': 1000}
    # Додайте інші стандартні розміри, якщо потрібно
]

def calculate_optimal_cuts(gate_width, gate_height):
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

    return optimal_layout

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

# Вхідні дані від користувача
gate_width = int(input("Введіть ширину воріт: "))
gate_height = int(input("Введіть висоту воріт: "))

# Розрахунок оптимального розміщення
optimal_layout = calculate_optimal_cuts(gate_width, gate_height)

# Виведення результатів
print("Кількість листів: ", optimal_layout['count'])
print("Розміщення на листах:")
print("Ширина\tДовжина\tКількість")
print(optimal_layout['width'], "\t", optimal_layout['length'], "\t", optimal_layout['count'])

input()
