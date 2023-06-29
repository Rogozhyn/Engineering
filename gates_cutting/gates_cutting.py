# This program helps to make cuttings of the sheets for the steel double gates.
# You need to enter gate size and point size of the steel sheet blank.
# After processing, you will receive most economical sheet cutting.

from math import ceil


class SheetBlank:
    def __init__(self, length, width, thickness):
        self.length = length  # mm
        self.width = width  # mm
        self.thickness = thickness  # mm
        self.init_area = length * width  # mm^2
        self.area = self.init_area  # mm^2

    def __str__(self):
        return f'Sheet {self.length} mm x {self.width} mm x {self.thickness} mm, {mm2_in_m2(self.area):.3f} m^2'


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
        return f'Ворота: {self.width} мм x {self.height} мм. Площа поверхні: {mm2_in_m2(self.area):.1f} м^2'

    def choose_sheets_by_thickness(self, sheets_catalog):
        for sheet in sheets_catalog.values():
            if sheet.get('thickness') == self.sheet_thickness:
                self.suitable_sheets_by_thickness.append(
                    (sheet.get('length'),
                     sheet.get('width'),
                     sheet.get('length') * sheet.get('width'))
                )
        self.suitable_sheets_by_thickness.sort(key=lambda sheet: sheet[2], reverse=True)
        print(f'Всього підходящих типорозмірів: {len(self.suitable_sheets_by_thickness)}')
        for item in self.suitable_sheets_by_thickness:
            print(f'Лист {item[0]} x {item[1]} x {self.sheet_thickness}')

    def calc_qty_sheets_by_area(self):
        # Якщо в списку підходящих листів нема жодного листа, то функція далі не виконується
        if len(self.suitable_sheets_by_thickness) == 0:
            print('Немає підходящих листів')
            return
        # Формуєму шаблон рядка для запису данних в список можливих варіантів
        # Для кожного типорозміру листа вказуємо кількість таких листів 0 одиниць
        line_entry = {'waste': None}
        for sheet in self.suitable_sheets_by_thickness:
            line_entry.update({sheet: 0})

        # Формуємо список в якому будемо записувати кількість листів для поточного прогону цикла while
        sheets_qty = [0] * len(self.suitable_sheets_by_thickness)

        # Проходимо циклом while варіант з кількістю листів в списку sheets_qty
        # и записуємо результати в список sheets_variants
        sheets_variants = []
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

            # Розраховуємо площу втраченого матеріалу
            waste_area = kit_area - self.area
            # Якщо площа, що буде втрачена більша за площу самих воріт, то розрахунок закінчується
            if waste_area > self.area:
                alive = False
            # Повністю копіюємо шаблон рядка для запису данних в таблицю розрахованних варіантів
            temp_line_entry = line_entry.copy()
            # Формуємо рядок з розрахованними данними для його подальшого додавання в список варіантів
            temp_line_entry['waste'] = round(mm2_in_m2(waste_area), 1)
            for i in range(len(self.suitable_sheets_by_thickness)):
                temp_line_entry[self.suitable_sheets_by_thickness[i]] = sheets_qty[i]
            # Додаємо сформованний рядок в список розрахованних варіантів
            sheets_variants.append(temp_line_entry)
            # print(temp_line_entry)
            # print(sheets_qty)

            # Якщо в списку підходящих типорозмірів всього один типорозмір, то подальший розрахунок не ведеться.
            # Якщо кількість листів всіх типорозмірів після першого дорівнює нулю, то це означає, що ми дійшли
            # до максимальної кількості листів першого типорозміру і подальші розрахунки не потрібні
            plus_one = False
            if len(self.suitable_sheets_by_thickness) == 1 or sum(sheets_qty[1:]) == 0:
                alive = False
            elif len(self.suitable_sheets_by_thickness) > 2:
                for item in range(len(sheets_qty) - 2):
                    # print(f'Item = {item}, sum = {sum(sheets_qty[item + 2:])}')
                    if sum(sheets_qty[item + 2:]) == 0:
                        sheets_qty[item + 1] = 0
                        sheets_qty[item] += 1
                        plus_one = False
                        break
                    else:
                        plus_one = True
            else:
                plus_one = True

            if plus_one:
                sheets_qty[-2] += 1

        sheets_variants.sort(key=lambda sheets: sheets['waste'])
        for item in sheets_variants:
            print(item)
        self.sheets_variants = sheets_variants


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
         'thickness': 5
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
         'thickness': 5
         },
    'size 7':
        {'length': 2500,
         'width': 1250,
         'thickness': 4
         },
    'size 8':
        {'length': 3000,
         'width': 1500,
         'thickness': 2
         },
}

gates = create_gates_mm(3255, 4355, 2)

print(gates)

gates.choose_sheets_by_thickness(standard_sizes)

gates.calc_qty_sheets_by_area()
