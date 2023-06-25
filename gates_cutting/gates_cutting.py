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
        self.init_square = length * width  # mm^2
        self.square = self.init_square  # mm^2
        self.init_weight = self.init_square * thickness * DENSITY
        self.weight = self.init_weight

    def __str__(self):
        return f'Sheet {self.length} mm x {self.width} mm x {self.thickness} mm,' \
               f' {self.weight / 1000000000:.1f} kg, {mm2_in_m2(self.square):.3f} m^2'


class Gates:
    def __init__(self, width, height, sheet_thickness):
        self.width = width
        self.half_width = width / 2
        self.height = height
        self.sheet_thickness = sheet_thickness
        self.square = self.width * self.height
        self.suitable_sheets_by_thickness = []
        self.sheets_variants = []

    def __str__(self):
        return f'Gates {self.width} mm x {self.height} mm, {mm2_in_m2(self.square)} m^2'

    def choose_sheets_by_thickness(self, sheets_catalog):
        for sheet in sheets_catalog.values():
            if sheet.get('thickness') == self.sheet_thickness:
                self.suitable_sheets_by_thickness.append(
                    (sheet.get('length'),
                     sheet.get('width'),
                     sheet.get('length') * sheet.get('width'))
                )
        print(f'Total sheet sizes: {len(self.suitable_sheets_by_thickness)}')

    def qty_sheets_by_square(self):
        line_entry = {'lost': None}

        for sheet in self.suitable_sheets_by_thickness:
            line_entry.update({sheet: 0})
        max_qty_table = []
        for sheet in self.suitable_sheets_by_thickness:
            qty_real = ceil(self.square / sheet[2])
            max_qty_table.append(qty_real)
            lost = qty_real * sheet[2] - self.square
            temp_line_entry = line_entry.copy()
            temp_line_entry['lost'] = lost
            temp_line_entry[sheet] = qty_real
            self.sheets_variants.append(temp_line_entry)
            print(temp_line_entry)


def mm2_in_m2(square_mm2):
    return square_mm2 / 1000000


def m2_in_mm2(square_m2):
    return square_m2 * 1000000


def create_sheet_mm(length, weight, thickness):
    return SheetBlank(length, weight, thickness)


def create_gates_mm(width, height, sheet_thickness):
    return Gates(width, height, sheet_thickness)


def create_gates_input():
    width = float(input('Enter Gates Width in mm: '))
    height = float(input('Enter Gates Height in mm: '))
    sheet_thickness = float(input('Enter Gates Sheet Thickness in mm: '))
    return Gates(width, height, sheet_thickness)


standard_sheets = {
    'size 1':
        {'length': 2500,
         'width': 1250,
         'thickness': 2
         },
    'size 2':
        {'length': 2000,
         'width': 1000,
         'thickness': 2
         },
    'size 3':
        {'length': 1000,
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
}

gates = create_gates_mm(3000, 3800, 2)

print(gates)

gates.choose_sheets_by_thickness(standard_sheets)

gates.qty_sheets_by_square()
