import os
from os import path


def make_files_dict(dir_path, file_suf, file_ext):
    # Makes dictionary with files and information about them
    files_dict = {}
    print(dir_path)
    for name in os.listdir(dir_path):
        full_path = path.join(dir_path, name)
        file_name = path.splitext(name)[0]  # without extension
        if path.isfile(full_path) and\
           path.splitext(full_path)[1][1:] == file_ext and\
           file_name.endswith("." + file_suf):
            files_dict[name] = {"full name": full_path,
                                "file name": file_name,
                                "head name": file_name.rstrip("." + file_suf),
                                "extension": path.splitext(name)[1][1:],
                                "file path": dir_path}
    if files_dict == {}:
        print('There are not *.{0}.{1} files. \n'.format(file_suf, file_ext))
    else:
        return files_dict


def make_new_name(input_dict):
    if input_dict is not None:
        print('New file names are:\n')
        for name in input_dict:
            print('{0}.{1}'.format(input_dict[name]['head name'], input_dict[name]['extension']))
        if input('\nRename? (yes/no): ') == 'yes':
            for name in input_dict:
                old_full_name = input_dict[name]['full name']
                new_full_name = path.join(input_dict[name]['file path'], (input_dict[name]['head name'] + '.' + input_dict[name]['extension']))
                os.rename(old_full_name, new_full_name)
        else:
            print('\nRename operation canceled.')


current_dir = os.getcwd()
list_to_do = (('idw', 'dwg'),
              ('idw', 'dwf'))
search_deep = int(input('Please enter index of search deep (1, 2): '))
# 1 - if it is need only files from current folder
# 2 - if it is need files from current folder and subfolders

if search_deep == 1:
    for task in list_to_do:
        dict_to_do = make_files_dict(current_dir, task[0], task[1])
        make_new_name(dict_to_do)
elif search_deep == 2:
    tree = os.walk(current_dir)
    for i in tree:
        for task in list_to_do:
            dict_to_do = make_files_dict(i[0], task[0], task[1])
            make_new_name(dict_to_do)
else:
    print('Please choise search deep')

input('Task is finished.\n\nPress ENTER')