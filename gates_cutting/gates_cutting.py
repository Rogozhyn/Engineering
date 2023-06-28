# This program helps to make cuttings of the sheets for the steel double gates.
# You need to enter gate size and point size of the steel sheet blank.
# After processing, you will receive most economical sheet cutting.

from math import ceil

DENSITY = 7850  # kg/m^3


class SheetBlank:
    def __init__(self, length, width, thickness):
        self.length = length  # mm
        self.width = width  # mm
        self.thickness = thickness  # mm
        self.init_area = length * width  # mm^2
        self.area = self.init_area  # mm^2
        self.init_weight = self.init_area * thickness * DENSITY
        self.weight = self.init_weight

    def __str__(self):
        return f'Sheet {self.length} mm x {self.width} mm x {self.thickness} mm,' \
               f' {self.weight / 1000000000:.1f} kg, {mm2_in_m2(self.area):.3f} m^2'


class Gates:
    def __init__(self, width, height, sheet_thickness):
        self.width = width
        self.half_width = width / 2
        self.height = height
        self.sheet_thickness = sheet_thickness
        self.area = self.width * self.height
        self.suitable_sheets_by_thickness = []
        self.sheets_variants = []

    def __str__(self):
        return f'Gates {self.width} mm x {self.height} mm, {mm2_in_m2(self.area)} m^2'

    def choose_sheets_by_thickness(self, sheets_catalog):
        for sheet in sheets_catalog.values():
            if sheet.get('thickness') == self.sheet_thickness:
                self.suitable_sheets_by_thickness.append(
                    (sheet.get('length'),
                     sheet.get('width'),
                     sheet.get('length') * sheet.get('width'))
                )
        print(f'Total sheet sizes: {len(self.suitable_sheets_by_thickness)}')

    def calc_qty_sheets_by_area(self):
        if len(self.suitable_sheets_by_thickness) == 0:
            return
        # Формуєму шаблон рядка для запису данних в список можливих варіантів
        # Для кожного типорозміру листа вказуємо кількість таких листів 0 одиниць
        line_entry = {'waste': None}
        for sheet in self.suitable_sheets_by_thickness:
            line_entry.update({sheet: 0})

        # Формуємо список в якому будемо записувати кількість листів для поточного прогону цикла while
        sheets_qty = [0] * len(self.suitable_sheets_by_thickness)

        # Проходимо циклом while варіант з кількістю листів в списку sheets_qty
        alive = True
        while alive:
            # Обнуляємо площу перед наступними розрахунками
            kit_area = 0

            # Розраховуємо площу всіх листів в списку підходящих типорозмірів листів, крім останнього.
            # Кількість листів останнього типорозміру будемо розраховувати окремо
            for i in range(len(self.suitable_sheets_by_thickness) - 1):
                kit_area += sheets_qty[i] * self.suitable_sheets_by_thickness[i][2]

            # Розраховуваємо яку площу повинні мати листи останнього типорозміру
            required_area = self.area - kit_area
            # Якщо вийде, що та площа, що мають листи крім останнього типорозміру вже більша, ніж площа воріт
            # то тоді кількість листів останнього типорозміру буде дорівнюватися нулю
            if required_area > 0:
                sheets_qty[-1] = ceil(required_area / self.suitable_sheets_by_thickness[-1][2])
            else:
                sheets_qty[-1] = 0
            kit_area += sheets_qty[-1] * self.suitable_sheets_by_thickness[-1][2]

            waste_area = kit_area - self.area
            # Якщо площа, що буде втрачена більша за площу самих воріт, то розрахунок закінчується
            if waste_area > self.area:
                alive = False
            # Повністю копіюємо шаблон рядка для запису данних в таблицю розрахованних варіантів
            temp_line_entry = line_entry.copy()
            # Формуємо рядок з розрахованними данними для його подальшого додавання в список варіантів
            temp_line_entry['waste'] = waste_area
            for i in range(len(self.suitable_sheets_by_thickness)):
                temp_line_entry[self.suitable_sheets_by_thickness[i]] = sheets_qty[i]
            # Додаємо сформованний рядок в список розрахованних варіантів
            self.sheets_variants.append(temp_line_entry)
            # print(temp_line_entry)
            print(sheets_qty)

            # Якщо в списку підходящих типорозмірів всього один типорозмір, то подальший розрахунок не ведеться.
            # Якщо кількість листів всіх типорозмірів після першого дорівнює нулю, то це означає, що ми дійшли
            # до максимальної кількості листів першого типорозміру і подальші розрахунки не потрібні
            if len(self.suitable_sheets_by_thickness) == 1 or sum(sheets_qty[1:]) == 0:
                alive = False
            else:
                for item_number in range(len(sheets_qty)-1):
                    pass

                sheets_qty[-2] += 1
                if sheets_qty[-1] == 0:
                    sheets_qty[-2] = 0

                    sheets_qty[-3] += 1


def mm2_in_m2(area_mm2):
    return area_mm2 / 1000000


def m2_in_mm2(area_m2):
    return area_m2 * 1000000


def create_gates_mm(width, height, sheet_thickness):
    return Gates(width, height, sheet_thickness)


def create_gates_input():
    width = float(input('Enter Gates Width in mm: '))
    height = float(input('Enter Gates Height in mm: '))
    sheet_thickness = float(input('Enter Gates Sheet Thickness in mm: '))
    return Gates(width, height, sheet_thickness)


standard_sizes = {
    'size 1':
        {'length': 2500,
         'width': 1250,
         'thickness': 2
         },
    'size 2':
        {'length': 1000,
         'width': 1000,
         'thickness': 2
         },
    'size 3':
        {'length': 2000,
         'width': 1000,
         'thickness': 2
         },
    'size 4':
        {'length': 2000,
         'width': 1000,
         'thickness': 3
         },
    'size 5':
        {'length': 2500,
         'width': 1250,
         'thickness': 3
         },
    'size 6':
        {'length': 1000,
         'width': 500,
         'thickness': 2
         },
    'size 7':
        {'length': 2500,
         'width': 1250,
         'thickness': 4
         },
}

gates = create_gates_mm(3000, 3800, 2)

print(gates)

gates.choose_sheets_by_thickness(standard_sizes)

gates.calc_qty_sheets_by_area()
