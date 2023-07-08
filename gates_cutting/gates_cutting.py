from math import ceil


class Gates:
    def __init__(self, width, height, sheet_thickness):
        self.width = width
        self.height = height
        self.area = self.width * self.height
        self.suitable_sheets_by_thickness = [(2500, 1250, 2500*1250),(2000, 1000, 2000*1000)]
        self.sheets_variants = []


    def calc_qty_sheets_by_area(self):
        sheets_qty = [0] * len(self.suitable_sheets_by_thickness)

        sheets_variants = []
        alive = True
        while alive:
            kit_area = 0
            temp_line_entry = {'waste': None, 'sheets': dict()}
            for i in range(len(self.suitable_sheets_by_thickness) - 1):
                kit_area += sheets_qty[i] * self.suitable_sheets_by_thickness[i][2]

            required_area = self.area - kit_area
            if required_area > 0:
                sheets_qty[-1] = ceil(required_area / self.suitable_sheets_by_thickness[-1][2])
            else:
                sheets_qty[-1] = 0
            kit_area += sheets_qty[-1] * self.suitable_sheets_by_thickness[-1][2]

            waste_area = kit_area - self.area
            waste_area_percentage = waste_area * 100 / self.area
            if waste_area > self.area:
                alive = False

            temp_line_entry['waste'] = round(waste_area_percentage, 1)
            for i in range(len(self.suitable_sheets_by_thickness)):
                temp_line_entry['sheets'][self.suitable_sheets_by_thickness[i]] = sheets_qty[i]
            sheets_variants.append(temp_line_entry)

            plus_one = False
            if len(self.suitable_sheets_by_thickness) == 1 or sum(sheets_qty[1:]) == 0:
                alive = False
            elif len(self.suitable_sheets_by_thickness) > 2:
                for item in range(len(sheets_qty) - 2):
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

        for item in sheets_variants:
            print(item)

        # sheets_variants.sort(key=lambda sheets: sheets['waste'])
        self.sheets_variants = sheets_variants


    def print_sheets_variants(self):
        if self.sheets_variants:
            print('Можливі наступні комбінації листів:')
            for count, value in enumerate(self.sheets_variants, start=1):
                print(f'{count}) Втрати {value["waste"]} %,')
                for sheet, qty in value['sheets'].items():
                    if qty != 0:
                        print(f'\t{sheet[0]} x {sheet[1]} - {qty} од.')
        elif not self.suitable_sheets_by_thickness:
            print('Список підходящих типорозмірів листів пустий. Завантажте список типорозмірів листів.')
        else:
            print('Список комбінацій листів пустий. Запустить розрахунок можливих комбінацій.')


standard_sizes = {
    'size 1':
        {'length': 2500,
         'width': 1250,
         'thickness': 2
         },
    'size 3':
        {'length': 2000,
         'width': 1000,
         'thickness': 2
         }
}

gates = Gates(3310, 3660, 2)

gates.calc_qty_sheets_by_area()
#gates.print_sheets_variants()
