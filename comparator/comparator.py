import os
from datetime import datetime

def make_names_dict(files_path):
    # Makes dictionary with all files information
    names_dict_def = {}
    for name in os.listdir(files_path):
        if os.path.isfile(os.path.join(files_path, name)):
            names_dict_def[name] = {"File name": os.path.splitext(name)[0],
                                    "File extension" : os.path.splitext(os.path.join(files_path, name))[1][1:],
                                    "File size" : os.path.getsize(os.path.join(files_path, name)),
                                    "File mod. time" : os.path.getmtime(os.path.join(files_path, name)),
                                    "File path": os.path.basename(files_path)}
            file_types_set.add(os.path.splitext(os.path.join(files_path, name))[1][1:])
    return names_dict_def


def make_list_without(main_type = "idw", slave_type = "pdf"):
    # Makes list with main files, which have not pairs of slave files
    print("\n{0} files without {1} files:\n{2}".format(main_type, slave_type, separator), file = file)
    if main_type and slave_type in extensions_dict:
        main_without_slave_list = sorted(list(set(extensions_dict[main_type]) - set(extensions_dict[slave_type])))
        if main_without_slave_list == []:
            print("Each {0} file has {1} file\n\n{2}".format(main_type, slave_type, separator), file = file)
        else:
            for number, name in enumerate(main_without_slave_list):
                print("{0:>3} : {1}".format(number+1, name), file = file)
            print("\n{}\n".format(separator), file = file)
            return {"main type" : main_type,
                "slave type" : slave_type,
                    "operation" : "main without slave",
                    "list" : main_without_slave_list}
    else:
        if main_type not in extensions_dict:
            print ("There are not {0} files".format(main_type), file = file)
        if slave_type not in extensions_dict:
            print ("There are not {0} files".format(slave_type), file = file)
        print("\n{}\n".format(separator), file = file)


def make_dict_with (main_type = "idw", slave_type = "pdf"):
    # Makes dictionary with main files, which have pairs of slave files
    print("\n{0} files with {1} files:\n{2}".format(main_type, slave_type, separator), file = file)
    if main_type and slave_type in extensions_dict:
        main_with_slave_dict = {}
        for number, name in enumerate(sorted(list(set(extensions_dict[main_type]) & set(extensions_dict[slave_type])))):
            main_with_slave_dict[name] = round((names_dict[name + "." + main_type]["File mod. time"] - 
                                                names_dict[name + "." + slave_type]["File mod. time"])/60)
            main_file_dir = names_dict[name + "." + main_type]["File path"]
            slave_file_dir = names_dict[name + "." + slave_type]["File path"]
            if main_file_dir == slave_file_dir:
                dirs = ""
            else:
                dirs = ' : "{0}" - "{1}"'.format(main_file_dir, slave_file_dir)
            print('{0:>3} : {1:<20} : {2:>5} minutes{3}'.format(number+1, name, main_with_slave_dict[name], dirs), file = file)
        print("\n{}\n".format(separator), file = file)
        return {"main type" : main_type,
                "slave type" : slave_type,
                "operation" : "main with slave",
                "dictionary" : main_with_slave_dict}
    else:
        if main_type not in extensions_dict:
            print ("There are not {0} files".format(main_type), file = file)
        if slave_type not in extensions_dict:
            print ("There are not {0} files".format(slave_type), file = file)
        print("\n{}\n".format(separator), file = file)


cur_path = os.getcwd()
cur_date = datetime.now().date()
cur_time = datetime.now().time()
cur_date_time = str(cur_date) + "_" + "{:0>2}".format(str(cur_time.hour)) +"{:0>2}".format(str(cur_time.minute))
file_name = "Result_" + cur_date_time + ".txt"
separator = "-----------------------------------------\n"
names_dict = {}
file_types_set = set()
list_to_do = (('idw', 'pdf'),
              ('iam', 'idw'),
              ('ipt', 'idw'),
              ('xls', 'pdf'),
             )


# Makes dictionary with all files information
# names_dict.update(make_names_dict(cur_path))
# for name in os.listdir(cur_path):
#     if os.path.isdir(os.path.join(cur_path, name)):
#         names_dict.update(make_names_dict(os.path.join(cur_path, name)))
names_dict.update(make_names_dict(cur_path))        

# Makes new dictionary with all extensions from set with all extensions
extensions_dict = {}
for type_ in file_types_set:
    extensions_dict[type_] = []
# Adds file names to the list linked with the key
for key in extensions_dict:
    for name in names_dict:
        if names_dict[name]["File extension"] == key:
            extensions_dict[key].append(names_dict[name]["File name"])

file = open(file_name, "w")

print("Date: {0}\nTime: {1:0>2}:{2:0>2}".format(str(cur_date),str(cur_time.hour), str(cur_time.minute)), file = file)
print("Curren directory: {}\n".format(cur_path), file = file)

for task in list_to_do:
    make_list_without(task[0], task[1])
    make_dict_with(task[0], task[1])

file.close()

print('The result you can find in the file "{}" in the current directory'.format(file_name))
input('\nPress Enter')