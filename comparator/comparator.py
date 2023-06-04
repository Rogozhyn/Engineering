import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

SEPARATOR = "\n" + 50 * "-" + "\n"
PROGRAM_NAME = "Files comparator"
PROGRAM_VERSION = "5.0"
TITLE = '{0} - ver. {1}'.format(PROGRAM_NAME, PROGRAM_VERSION)
chosen_path = None


def get_current_time(*args):
    cur_date = datetime.now().date()
    cur_time = datetime.now().time()
    if 'date' in args and 'time' not in args:
        return str(cur_date)
    elif 'time' in args and 'date' not in args:
        return "{0:0>2}:{1:0>2}".format(str(cur_time.hour), str(cur_time.minute))
    elif 'date' in args and 'time' in args:
        return "{0} {1:0>2}:{2:0>2}".format(str(cur_date), str(cur_time.hour), str(cur_time.minute))
    else:
        return str(cur_date) + "_" + "{:0>2}".format(str(cur_time.hour)) + "{:0>2}".format(str(cur_time.minute))


def get_file_name():
    return "Result_" + get_current_time() + ".txt"


def get_absolute_file_name(file_path):
    return os.path.join(file_path, get_file_name())


def on_rad_search_depth():
    print(search_depth.get())


def make_search_depth(search_path, search_depth):
    # Makes dictionary with all files information
    if search_depth == 1:
        names_dict.update(make_names_dict(search_path))
    elif search_depth == 2:
        tree = os.walk(search_path)
        for path in tree:
            names_dict.update(make_names_dict(path[0]))
    elif search_depth == 3:
        tree_1 = os.walk(os.path.join(search_path, '02_CAD Data'))
        for path in tree_1:
            names_dict.update(make_names_dict(path[0]))
        tree_2 = os.walk(os.path.join(search_path, '05_2D Drawings PDF'))
        tree_list = []
        for path in tree_2:
            tree_list.append(path[0])
            names_dict.update(make_names_dict(tree_list[-1]))
    elif search_depth == 4:
        tree_1 = os.walk(os.path.join(search_path, '02_CAD Data'))
        for path in tree_1:
            names_dict.update(make_names_dict(path[0]))
        tree_2 = os.walk(os.path.join(search_path, '09_Project kit\\01_PDF'))
        for path in tree_2:
            names_dict.update(make_names_dict(path[0]))


def make_list_todo():
    list_todo = (('idw', 'pdf'),
                 ('ipt', 'idw'),
                 ('xls', 'pdf'),
                 ('idw', 'dwg'),
                 ('idw', 'dwf'),
                 )
    return list_todo


def make_names_dict(files_path):
    # Makes dictionary with all files information
    names_dict_in_def = {}
    for name in os.listdir(files_path):
        absolute_file_name = os.path.join(files_path, name)
        if os.path.isfile(absolute_file_name):
            names_dict_in_def[name] = {"File name": os.path.splitext(name)[0],
                                       "File extension": os.path.splitext(absolute_file_name)[1][1:],
                                       "File size": os.path.getsize(absolute_file_name),
                                       "File mod. time": os.path.getmtime(absolute_file_name),
                                       "File path": os.path.basename(files_path)}
            file_types_set.add(os.path.splitext(absolute_file_name)[1][1:])
    return names_dict_in_def


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
    print("{2}{0} files without {1} files:{2}".format(main_type, slave_type, SEPARATOR), file=logfile)
    if (main_type in extensions_dict) and (slave_type in extensions_dict):
        main_without_slave_list = sorted(list(set(extensions_dict[main_type]) - set(extensions_dict[slave_type])))
        if not main_without_slave_list:
            print("Each {0} file has {1} file\n{2}".format(main_type, slave_type, SEPARATOR), file=logfile)
        else:
            for number, name in enumerate(main_without_slave_list):
                print("{0:>3} : {1}".format(number + 1, name), file=logfile)
            print(SEPARATOR, file=logfile)
            return {"main type": main_type,
                    "slave type": slave_type,
                    "operation": "main without slave",
                    "list": main_without_slave_list}
    else:
        if main_type not in extensions_dict:
            print("There are not {0} files".format(main_type), file=logfile)
        if slave_type not in extensions_dict:
            print("There are not {0} files".format(slave_type), file=logfile)
        print(SEPARATOR, file=logfile)


def make_dict_with(main_type, slave_type):
    # Makes dictionary with main files, which have pairs of slave files
    print("{2}{0} files with {1} files:{2}".format(main_type, slave_type, SEPARATOR), file=logfile)
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
            print('{0:>3} : {1:<25} : {2:>7} minutes{3}'.format(number + 1, name, main_with_slave_dict[name], dirs),
                  file=logfile)
        print(SEPARATOR, file=logfile)
        return {"main type": main_type,
                "slave type": slave_type,
                "operation": "main with slave",
                "dictionary": main_with_slave_dict}
    else:
        if main_type not in extensions_dict:
            print("There are not {0} files".format(main_type), file=logfile)
        if slave_type not in extensions_dict:
            print("There are not {0} files".format(slave_type), file=logfile)
        print(SEPARATOR, file=logfile)


def main(search_path, search_depth):
    global logfile
    base_logfile_name = get_file_name()
    full_logfile_name = get_absolute_file_name(search_path)
    logfile = open(full_logfile_name, "w")
    print("Date: {}".format(get_current_time('date')), file=logfile)
    print("Time: {}".format(get_current_time('time')), file=logfile)
    print("Start directory: {}\n".format(search_path), file=logfile)

    make_search_depth(search_path, search_depth)
    make_extensions_dict()

    list_todo = make_list_todo()
    for task in list_todo:
        make_list_without(task[0], task[1])
        make_dict_with(task[0], task[1])

    if 'pdf' in extensions_dict.keys():
        print('Total: ', len(extensions_dict['pdf']), ' pdf files.', file=logfile)

    logfile.close()

    open_folder = messagebox.askyesno('Open start folder?', 'The result you can find in the file'
                                                            '\n " {} "\n'
                                                            'from the start folder.\n\n'
                                                            'Open start folder?'.format(base_logfile_name))
    if open_folder:
        os.startfile(search_path)
    os.startfile(full_logfile_name)


def on_btn_choose_folder():
    folder = filedialog.askdirectory()
    entry_path.delete(0, "end")
    entry_path.insert(0, folder)


def on_btn_run():
    global chosen_path
    path = entry_path.get()
    if os.path.isdir(path):
        chosen_path = path
        main(chosen_path, search_depth.get())
    else:
        messagebox.showwarning('Warning',
                               'The path of the specified start folder is incorrect.\nPlease specify the correct folder')


names_dict = {}
extensions_dict = {}
file_types_set = set()
current_path = os.getcwd()

root = tk.Tk()
root.title(TITLE)
widget_row = 0
tk.Label(root, text='Step 1 - Specify or select a start folder:').grid(row=widget_row, column=0,
                                                                       padx=5, pady=10, sticky='w')

widget_row += 1
entry_path = tk.Entry(root, width=125)
entry_path.insert(0, current_path)
entry_path.grid(row=widget_row, column=0, padx=5, pady=10, sticky='w')
entry_path.focus()

btn_choose_folder = tk.Button(root, text="Choose folder", command=on_btn_choose_folder)
btn_choose_folder.grid(row=widget_row, column=1, padx=5, sticky='e')

widget_row += 1
tk.Label(root, text='Step 2 - Select search depth:').grid(row=widget_row, column=0, padx=5, pady=10, sticky='w')

widget_row += 1
search_depth = tk.IntVar()
search_depth.set(1)
search_depth_variants = {1: 'to search files only from selected folder',
                         2: 'to search files only from selected folder and sub-folders',
                         3: 'to search files in folders 02_CAD and 05_PDF',
                         4: 'to search files in folders 02_CAD and 09_Project kit',
                         }
for key in search_depth_variants:
    widget_row += 1
    tk.Radiobutton(root, text=search_depth_variants[key], value=key, variable=search_depth,
                   command=on_rad_search_depth).grid(row=widget_row, column=0, sticky='w')

widget_row += 1
tk.Label(root, text='Step 3 - Specify pairs of extensions to search:').grid(row=widget_row, column=0,
                                                                            padx=5, pady=10, sticky='w')

widget_row += 1
tk.Label(root, text='Step 4 - Run search.').grid(row=widget_row, column=0, padx=5, pady=10, sticky='w')

widget_row += 1
btn_run = tk.Button(root, text='RUN', command=on_btn_run)
btn_run.grid(row=widget_row, column=0)

root.mainloop()
