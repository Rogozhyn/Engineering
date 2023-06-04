import os

cur_path = os.getcwd()
#cur_path = "C:\\Users\\mrogozhyn\\Desktop\\test folder\\folder 1\\folder 1_1"

print("Curren directory:\n", cur_path,)
print("\nCurren directory files and folders:\n---------------------------------------")
for item in os.listdir(cur_path):
    print(item)
print("---------------------------------------\n")

names_dict = {}
for name in os.listdir(cur_path):
    if os.path.isfile(os.path.join(cur_path, name)):
        names_dict[name] = {"File name": os.path.splitext(name)[0],
                            "File extension" : os.path.splitext(os.path.join(cur_path, name))[1][1:],
                            "File size" : os.path.getsize(os.path.join(cur_path, name)),
                            "File mod. time" : os.path.getmtime(os.path.join(cur_path, name))}

file_types_list = ["idw", "pdf", "dwg"]

extensions_dict = {}
for number in range(len(file_types_list)):
    extensions_dict[file_types_list[number - 1]] = []

for key in extensions_dict:
    for name in names_dict:
        if names_dict[name]["File extension"] == key:
            extensions_dict[key].append(names_dict[name]["File name"])

for key in extensions_dict:
    print(key, " files: ", extensions_dict[key], "| total: ", len(extensions_dict[key]))

idw_with_pdf_list = list(set(extensions_dict["idw"]) & set(extensions_dict["pdf"]))
print("\nidw files with pdf files:\n---------------------------------------")
for item in idw_with_pdf_list:
    print(item)
print("---------------------------------------\n")

idw_without_pdf_list = list(set(extensions_dict["idw"]) - set(extensions_dict["pdf"]))
print("idw files without pdf files:\n---------------------------------------")
for item in idw_without_pdf_list:
    print(item)
print("---------------------------------------\n")

idw_with_dwg_list = list(set(extensions_dict["idw"]) & set(extensions_dict["dwg"]))
print("idw files with dwg files:\n---------------------------------------")
for item in idw_with_dwg_list:
    print(item)
print("---------------------------------------\n")

idw_without_dwg_list = list(set(extensions_dict["idw"]) - set(extensions_dict["dwg"]))
print("idw files without dwg files:\n---------------------------------------")
for item in idw_without_dwg_list:
    print(item)
print("---------------------------------------\n")

input('')
