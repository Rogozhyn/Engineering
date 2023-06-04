# This program helps to make cuttings of the sheets for the steel double gates.
# You need to enter gate size and point size of the steel sheet blank.
# After processing, you will receive most economical sheet cutting.
# All dimensions under hood are in m (meter)

DENSITY = 7850  # kg/m^3


class SheetBlank:
    def __init__(self, length, width, thickness):
        self.length = length  # m
        self.width = width  # m
        self.thickness = thickness  # m
        self.init_square = length * width  # m^2
        self.square = self.init_square  # m^2
        self.init_weight = self.init_square * thickness * DENSITY
        self.weight = self.init_weight

    def __str__(self):
        return f'Sheet {self.length:.3f} m x {self.width:.3f} m x {self.thickness:.3f} m, {self.weight:.1f} kg, {self.square:.1f} m^2'


class Gates:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.square = self.width * self.height

    def __str__(self):
        return f'Gates {self.width:.3f} m x {self.height:.3f} m, {self.square:.1f} m^2'


def create_sheet_mm(length, weight, thickness):
    return SheetBlank(length * 0.001, weight * 0.001, thickness * 0.001)


def create_gates_mm(width, height):
    return Gates(width * 0.001, height * 0.001)


def create_gates_input():
    width = float(input('Enter Gates Width in mm: '))
    height = float(input('Enter Gates Height in mm: '))
    return Gates(width * 0.001, height * 0.001)


standard_sheets = {
    'size 1':
        {'length': 2500,
         'weight': 1250,
         'thickness': 2
         },
    'size 2':
        {'length': 2000,
         'weight': 1000,
         'thickness': 2
         },
}

sheets = []
for sheet in standard_sheets.values():
    sheets.append(create_sheet_mm(sheet.get('length'), sheet.get('weight'), sheet.get('thickness')))

for sheet in sheets:
    print(sheet)

gates = create_gates_input()

print(gates)
