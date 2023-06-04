import os

cur_path = os.getcwd()

print("Текущая деректория:", cur_path)

names = [name for name in os.listdir(cur_path) if os.path.isfile(name)]
names_idw = [name for name in names if name.endswith('.idw')]
names_pdf = [name for name in names if name.endswith('.pdf')]

print("\nList of the all types of the files:")
for name in names:
    print(name)
print("\nList of the pdf type of the files:")
for name in names_pdf:
    print(name)
print("\nList of the idw type of the files:")
for name in names_idw:
    print(name)


""" names_dict = {}
for name in names_idw:
    names_dict[name.rstrip(".idw")] = ["idw"]
for name in names_pdf:
    names_dict[name.rstrip(".pdf")].append("pdf")

print(names_dict)
     """

input('')