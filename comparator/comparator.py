import os

cur_path = os.getcwd()
#cur_path = "C:\\Users\\mrogozhyn\\Desktop\\test folder\\folder 1\\folder 1_1"

print("Curren directory:\n", cur_path,)


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

main_with_second_list = list(set(extensions_dict[file_types_list[0]]) & set(extensions_dict[file_types_list[1]]))
print("\n {0} files with {1} files:\n---------------------------------------".format(file_types_list[0], file_types_list[1]))
for item in main_with_second_list:
    print(item)
print("---------------------------------------\n")

main_without_second_list = list(set(extensions_dict[file_types_list[0]]) - set(extensions_dict[file_types_list[1]]))
print("\n {0} files without {1} files:\n---------------------------------------".format(file_types_list[0], file_types_list[1]))
for item in main_without_second_list:
    print(item)
print("---------------------------------------\n")

main_with_third_list = list(set(extensions_dict[file_types_list[0]]) & set(extensions_dict[file_types_list[2]]))
print("\n {0} files with {1} files:\n---------------------------------------".format(file_types_list[0], file_types_list[2]))
for item in main_with_third_list:
    print(item)
print("---------------------------------------\n")

main_without_third_list = list(set(extensions_dict[file_types_list[0]]) - set(extensions_dict[file_types_list[2]]))
print("\n {0} files without {1} files:\n---------------------------------------".format(file_types_list[0], file_types_list[2]))
for item in main_without_third_list:
    print(item)
print("---------------------------------------\n")

input('')
