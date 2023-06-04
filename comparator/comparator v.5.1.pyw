import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

SEPARATOR = "\n" + 50 * "-" + "\n"
PROGRAM_NAME = "Files comparator"
PROGRAM_VERSION = "5.1"
TITLE = '{0} - ver. {1}'.format(PROGRAM_NAME, PROGRAM_VERSION)
chosen_path = None
list_todo = [['idw', 'pdf'],
             ['ipt', 'idw'],
             ['xls', 'pdf'],
             ['idw', 'dwg'],
             ['idw', 'dwf'],
             ]


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


def make_search_on_depth(search_path, search_depth):
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
    global logfile, list_todo
    base_logfile_name = get_file_name()
    full_logfile_name = get_absolute_file_name(search_path)
    logfile = open(full_logfile_name, "w")
    print("Date: {}".format(get_current_time('date')), file=logfile)
    print("Time: {}".format(get_current_time('time')), file=logfile)
    print("Start directory: {}\n".format(search_path), file=logfile)

    make_search_on_depth(search_path, search_depth)
    make_extensions_dict()

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


def on_rad_search_depth():
    print(search_depth.get())


def on_row_del_btn(item):
    global todo_frame, input_todo_frame
    list_todo.pop(item)
    todo_frame.grid_remove()
    input_todo_frame.grid_remove()
    make_todo_frame(row_for_todo_frame)
    make_input_todo_frame(row_for_input_todo_frame, last_row)


def on_row_add_btn():
    global todo_frame, input_todo_frame, list_todo, new_row
    main_type = new_row[0].get()
    slave_type = new_row[1].get()
    if main_type and slave_type:
        list_todo.append([main_type, slave_type])
        todo_frame.grid_remove()
        input_todo_frame.grid_remove()
        make_todo_frame(row_for_todo_frame)
        make_input_todo_frame(row_for_input_todo_frame, last_row)


def check_list_todo():
    global list_todo
    if list_todo:
        return True
    else:
        messagebox.showwarning('Warning',
                               'Specify at least one pair of file extensions\n to compare (see Step 3)')


def check_entry_path():
    if os.path.isdir(entry_path.get()):
        return entry_path.get()
    else:
        messagebox.showwarning('Warning',
                               'The path of the specified start folder is incorrect.\n'
                               'Please specify the correct folder (see Step 1)')
        return False


def check_search_depth():
    if search_depth.get() == 3:
        check_search_depth_3()
    elif search_depth.get() == 4:
        check_search_depth_4()
    else:
        return True


def check_search_depth_3():
    chosen_path = check_entry_path()
    dir_1 = os.path.isdir(os.path.join(chosen_path, '02_CAD Data'))
    dir_2 = os.path.isdir(os.path.join(chosen_path, '05_2D Drawings PDF'))
    if dir_1 and dir_2:
        return True
    elif dir_1 and not dir_2:
        messagebox.showwarning('Warning',
                               'The folder "05_2D Drawings PDF" does not exist.\n'
                               'Please change the search depth (see Step 3)')
        return False
    elif not dir_1 and dir_2:
        messagebox.showwarning('Warning',
                               'The folder "02_CAD Data" does not exist.\n'
                               'Please change the search depth (see Step 3)')
        return False
    else:
        messagebox.showwarning('Warning',
                               'The folders "02_CAD Data" and "05_2D Drawings PDF" do not exist.\n'
                               'Please change the search depth (see Step 3)')
        return False


def check_search_depth_4():
    chosen_path = check_entry_path()
    dir_1 = os.path.isdir(os.path.join(chosen_path, '02_CAD Data'))
    dir_2 = os.path.isdir(os.path.join(chosen_path, '09_Project kit'))
    if dir_1 and dir_2:
        return True
    elif dir_1 and not dir_2:
        messagebox.showwarning('Warning',
                               'The folder "09_Project kit" does not exist.\n'
                               'Please change the search depth (see Step 3)')
        return False
    elif not dir_1 and dir_2:
        messagebox.showwarning('Warning',
                               'The folder "02_CAD Data" does not exist.\n'
                               'Please change the search depth (see Step 3)')
        return False
    else:
        messagebox.showwarning('Warning',
                               'The folders "02_CAD Data" and "09_Project kit" do not exist.\n'
                               'Please change the search depth (see Step 3)')
        return False


def on_btn_run():
    global chosen_path
    if check_list_todo() and check_entry_path() and check_search_depth():
        chosen_path = check_entry_path()
        main(chosen_path, search_depth.get())


def make_todo_frame(row_number):
    global todo_frame, frame_widgets_list, list_todo, last_row
    if list_todo:
        todo_frame = tk.Frame(root)
        todo_frame.grid(row=row_number, column=0, sticky='w')
        frame_widgets_list = []
        for number, pair in enumerate(list_todo):
            tk.Label(todo_frame, text='{}) '.format(number + 1)).grid(row=number, column=0, padx=5, pady=5)
            temp_list = []
            temp_list.append(tk.Entry(todo_frame, width=8))
            temp_list[0].grid(row=number, column=1)
            temp_list[0].insert(0, pair[0])
            temp_list[0]['state'] = 'disable'
            tk.Label(todo_frame, text=' - ').grid(row=number, column=2, padx=5)
            temp_list.append(tk.Entry(todo_frame, width=8))
            temp_list[1].grid(row=number, column=3)
            temp_list[1].insert(0, pair[1])
            temp_list[1]['state'] = 'disable'
            temp_list.append(tk.Button(todo_frame, text='Delete', width=6))
            temp_list[2].grid(row=number, column=4, padx=5)
            temp_list[2]['command'] = lambda item=number: on_row_del_btn(item)
            frame_widgets_list.append(temp_list)
        last_row = len(list_todo)+1
    else:
        last_row = 1


def make_input_todo_frame(start_row, last_row):
    global input_todo_frame, new_row
    input_todo_frame = tk.Frame(root)
    input_todo_frame.grid(row=start_row, column=0, sticky='w')
    new_row = []
    tk.Label(input_todo_frame, text='{}) '.format(last_row)).grid(row=0, column=0, padx=5, pady=5)

    new_row.append(tk.Entry(input_todo_frame, width=8))
    new_row[0].grid(row=0, column=1, sticky='w')
    tk.Label(input_todo_frame, text=' - ').grid(row=0, column=2, padx=5, sticky='w')

    new_row.append(tk.Entry(input_todo_frame, width=8))
    new_row[1].grid(row=0, column=3, sticky='w')

    new_row.append(tk.Button(input_todo_frame, text='Add', width=6, command=on_row_add_btn))
    new_row[2].grid(row=0, column=4, padx=5)


names_dict = {}
extensions_dict = {}
file_types_set = set()
current_path = os.getcwd()

root = tk.Tk()
root.title(TITLE)
widgets_row = 0
tk.Label(root, text='Step 1 - Specify or select a start folder:').grid(row=widgets_row, column=0,
                                                                       padx=5, pady=10, sticky='w')

widgets_row += 1
entry_path = tk.Entry(root, width=125)
entry_path.insert(0, current_path)
entry_path.grid(row=widgets_row, column=0, padx=5, pady=10, sticky='w')
entry_path.focus()

btn_choose_folder = tk.Button(root, text="Choose folder", command=on_btn_choose_folder)
btn_choose_folder.grid(row=widgets_row, column=1, padx=5, sticky='e')

widgets_row += 1
tk.Label(root, text='Step 2 - Select search depth:').grid(row=widgets_row, column=0, padx=5, pady=10, sticky='w')

widgets_row += 1
search_depth = tk.IntVar()
search_depth.set(1)
search_depth_variants = {1: 'to search files only in start folder',
                         2: 'to search files in start folder and all sub-folders',
                         3: 'to search files in start folder and folders 02_CAD and 05_2D Drawings PDF',
                         4: 'to search files in start folder and folders 02_CAD and 09_Project kit',
                         }
for key in search_depth_variants:
    widgets_row += 1
    tk.Radiobutton(root, text=search_depth_variants[key], value=key, variable=search_depth,
                   command=on_rad_search_depth).grid(row=widgets_row, column=0, sticky='w')

widgets_row += 1
tk.Label(root, text='Step 3 - Specify pairs of extensions to search as "master type - slave type":')\
    .grid(row=widgets_row, column=0, padx=5, pady=10, sticky='w')
widgets_row += 1
row_for_todo_frame = widgets_row
make_todo_frame(row_for_todo_frame)

widgets_row += 1
row_for_input_todo_frame = widgets_row
make_input_todo_frame(row_for_input_todo_frame, last_row)

widgets_row += 1
tk.Label(root, text='Step 4 - Run search.').grid(row=widgets_row, column=0, padx=5, pady=10, sticky='w')

widgets_row += 1
btn_run = tk.Button(root, text='RUN', width=20, command=on_btn_run)
btn_run.grid(row=widgets_row, column=0, pady=10)

root.resizable(False, False)
root.mainloop()
