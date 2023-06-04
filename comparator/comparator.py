import os

def make_list_without(main_type = "idw", slave_type = "pdf"):
    # Makes list with main files, which have not pairs of slave files
    print("\n{0} files without {1} files:\n---------------------------------------".format(main_type, slave_type))
    if main_type and slave_type in extensions_dict:
        main_without_slave_list = sorted(list(set(extensions_dict[main_type]) - set(extensions_dict[slave_type])))
        for number, name in enumerate(main_without_slave_list):
            print("{0:>3} : {1}".format(number+1, name))
        print("---------------------------------------\n")
        return {"main type" : main_type, "slave type" : slave_type, "operation" : "main without slave", "list" : main_without_slave_list}
    else:
        if main_type not in extensions_dict:
            print ("There are not {0} files".format(main_type))
        if slave_type not in extensions_dict:
            print ("There are not {0} files".format(slave_type))
        print("---------------------------------------\n")

def make_dict_with (main_type = "idw", slave_type = "pdf"):
    # Makes dictionary with main files, which have pairs of slave files
    print("\n{0} files with {1} files:\n---------------------------------------".format(main_type, slave_type))
    if main_type and slave_type in extensions_dict:
        main_with_slave_dict = {}
        for number, name in enumerate(sorted(list(set(extensions_dict[main_type]) & set(extensions_dict[slave_type])))):
            main_with_slave_dict[name] = round((names_dict[name + "." + main_type]["File mod. time"] - names_dict[name + "." + slave_type]["File mod. time"])/60)
            print("{0:>3} : {1:<20} : {2:>5} minutes".format(number+1, name, main_with_slave_dict[name]))
        print("---------------------------------------\n")
        return {"main type" : main_type, "slave type" : slave_type, "operation" : "main with slave", "dictionary" : main_with_slave_dict}
    else:
        if main_type not in extensions_dict:
            print ("There are not {0} files".format(main_type))
        if slave_type not in extensions_dict:
            print ("There are not {0} files".format(slave_type))
        print("---------------------------------------\n")

cur_path = os.getcwd()

print("Curren directory:\n", cur_path,)

# Makes dictionary with all files information
names_dict = {}
file_types_set = set()
for name in os.listdir(cur_path):
    if os.path.isfile(os.path.join(cur_path, name)):
        names_dict[name] = {"File name": os.path.splitext(name)[0],
                            "File extension" : os.path.splitext(os.path.join(cur_path, name))[1][1:],
                            "File size" : os.path.getsize(os.path.join(cur_path, name)),
                            "File mod. time" : os.path.getmtime(os.path.join(cur_path, name))}
        file_types_set.add(os.path.splitext(os.path.join(cur_path, name))[1][1:])

# Makes new dictionary with all extensions from set with all extensions
extensions_dict = {}
for type_ in file_types_set:
    extensions_dict[type_] = []

# Adds file names to the list linked with the key
for key in extensions_dict:
    for name in names_dict:
        if names_dict[name]["File extension"] == key:
            extensions_dict[key].append(names_dict[name]["File name"])

idw_without_pdf = make_list_without()
idw_with_pdf = make_dict_with()
idw_without_dwg = make_list_without("idw", "dwg")
idw_with_dwg = make_dict_with("idw", "dwg")

input('')