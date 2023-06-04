import os
from datetime import datetime


def make_names_dict(files_path):
    # Makes dictionary with all files information
    names_dict_def = {}
    for name in os.listdir(files_path):
        if os.path.isfile(os.path.join(files_path, name)):
            names_dict_def[name] = {"File name": os.path.splitext(name)[0],
                                    "File extension": os.path.splitext(os.path.join(files_path, name))[1][1:],
                                    "File size": os.path.getsize(os.path.join(files_path, name)),
                                    "File mod. time": os.path.getmtime(os.path.join(files_path, name)),
                                    "File path": os.path.basename(files_path)}
            file_types_set.add(os.path.splitext(os.path.join(files_path, name))[1][1:])
    return names_dict_def


def get_search_deep():
    global search_deep
    print('''
         1 - if it is need only files from current folder
         2 - if it is need files from current folder and sub-folders
         3 - if it is need to search files in folders 02_CAD and 05_PDF
         4 - if it is need to search files in folder 02_CAD and 09_Project kit
            ''')
    search_deep = int(input('Please enter index of search deep (1, 2, 3, 4): '))


def make_search_deep():
    # Makes dictionary with all files information
    if search_deep == 1:
        names_dict.update(make_names_dict(work_path))
    elif search_deep == 2:
        tree = os.walk(work_path)
        for i in tree:
            names_dict.update(make_names_dict(i[0]))
    elif search_deep == 3:
        tree_1 = os.walk(os.path.join(work_path, '02_CAD Data'))
        for i in tree_1:
            names_dict.update(make_names_dict(i[0]))
        tree_2 = os.walk(os.path.join(work_path, '05_2D Drawings PDF'))
        tree_list = []
        for i in tree_2:
            tree_list.append(i[0])
            names_dict.update(make_names_dict(tree_list[-1]))
        print('\nEnd search folder is: \n{}\n'.format(tree_list[-1]))
    elif search_deep == 4:
        tree_1 = os.walk(os.path.join(work_path, '02_CAD Data'))
        for i in tree_1:
            names_dict.update(make_names_dict(i[0]))
        tree_2 = os.walk(os.path.join(work_path, '09_Project kit\\01_PDF'))
        for i in tree_2:
            names_dict.update(make_names_dict(i[0]))
    else:
        print('Please chose search deep')


def make_extensions_dict():
    # Makes new dictionary with all extensions from set with all extensions
    for type_ in file_types_set:
        extensions_dict[type_] = []
    # Adds file names to the list linked with the key
    for key in extensions_dict:
        for name in names_dict:
            if names_dict[name]["File extension"] == key:
                extensions_dict[key].append(names_dict[name]["File name"])


def make_list_without(main_type, slave_type):
    # Makes list with main files, which have not pairs of slave files
    print("\n{0} files without {1} files:\n{2}".format(main_type, slave_type, separator), file=file)
    if (main_type in extensions_dict) and (slave_type in extensions_dict):
        main_without_slave_list = sorted(list(set(extensions_dict[main_type]) - set(extensions_dict[slave_type])))
        if not main_without_slave_list:
            print("Each {0} file has {1} file\n\n{2}".format(main_type, slave_type, separator), file=file)
        else:
            for number, name in enumerate(main_without_slave_list):
                print("{0:>3} : {1}".format(number + 1, name), file=file)
            print("\n{}\n".format(separator), file=file)
            return {"main type": main_type,
                    "slave type": slave_type,
                    "operation": "main without slave",
                    "list": main_without_slave_list}
    else:
        if main_type not in extensions_dict:
            print("There are not {0} files".format(main_type), file=file)
        if slave_type not in extensions_dict:
            print("There are not {0} files".format(slave_type), file=file)
        print("\n{}\n".format(separator), file=file)


def make_dict_with(main_type, slave_type):
    # Makes dictionary with main files, which have pairs of slave files
    print("\n{0} files with {1} files:\n{2}".format(main_type, slave_type, separator), file=file)
    if (main_type in extensions_dict) and slave_type in extensions_dict:
        main_with_slave_dict = {}
        for number, name in enumerate(sorted(list(set(extensions_dict[main_type]) & set(extensions_dict[slave_type])))):
            main_with_slave_dict[name] = round((names_dict[name + "." + main_type]["File mod. time"] -
                                                names_dict[name + "." + slave_type]["File mod. time"]) / 60)
            main_file_dir = names_dict[name + "." + main_type]["File path"]
            slave_file_dir = names_dict[name + "." + slave_type]["File path"]
            if main_file_dir == slave_file_dir:
                dirs = ""
            else:
                dirs = ' : "{0}" - "{1}"'.format(main_file_dir, slave_file_dir)
            print('{0:>3} : {1:<20} : {2:>5} minutes{3}'.format(number + 1, name, main_with_slave_dict[name], dirs),
                  file=file)
        print("\n{}\n".format(separator), file=file)
        return {"main type": main_type,
                "slave type": slave_type,
                "operation": "main with slave",
                "dictionary": main_with_slave_dict}
    else:
        if main_type not in extensions_dict:
            print("There are not {0} files".format(main_type), file=file)
        if slave_type not in extensions_dict:
            print("There are not {0} files".format(slave_type), file=file)
        print("\n{}\n".format(separator), file=file)


def make_list_todo():
    global list_todo
    list_todo = (('idw', 'pdf'),
                 ('ipt', 'idw'),
                 ('xls', 'pdf'),
                 ('idw', 'dwg'),
                 ('idw', 'dwf'),
                 )
    return list_todo


def main():
    print("Date: {0}\nTime: {1:0>2}:{2:0>2}".format(str(cur_date), str(cur_time.hour), str(cur_time.minute)), file=file)
    print("Current directory: {}\n".format(work_path), file=file)

    get_search_deep()
    make_search_deep()
    make_extensions_dict()

    for task in make_list_todo():
        make_list_without(task[0], task[1])
        make_dict_with(task[0], task[1])

    if 'pdf' in extensions_dict.keys():
        print('Total: ', len(extensions_dict['pdf']), ' pdf files.', file=file)

    file.close()

    print('The result you can find in the file "{}" in the current directory'.format(file_name))
    input('\nPress Enter')


current_path = os.getcwd()
# work_path = R'C:\Users\mrogozhyn\Desktop\test folder\folder 1\folder 1_1'
work_path = current_path
# work_path = input('Enter path: ')

cur_date = datetime.now().date()
cur_time = datetime.now().time()
cur_date_time = str(cur_date) + "_" + "{:0>2}".format(str(cur_time.hour)) + "{:0>2}".format(str(cur_time.minute))

file_name = os.path.join(work_path, ("Result_" + cur_date_time + ".txt"))
file = open(file_name, "w")

separator = "-----------------------------------------\n"
names_dict = {}
extensions_dict = {}
file_types_set = set()
list_todo = tuple()
search_deep = 1

if __name__ == '__main__':
    main()
