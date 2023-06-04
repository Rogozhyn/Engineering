import os  # use "os.rename"
import re  # use "re.sub"
from os import path  # use "path.join"
from glob import glob  # use "glob"

SEPARATOR = '-' * 50


def rename_files(file_ext):
    '''
    This function make list of files with extension from file_ext parameter with help of "glob".
    Then the function receives pattern of part of file name from user and new part of the file name.
    Do this with "re.sub".
    After that function makes new list with all new file names.
    If user agree with new file names in the list, the function rename files with "os.rename".
    '''
    # receive list of files with extention from parameter "file_ext"
    input_files_list = glob(f'*.{file_ext}')
    if input_files_list:
        old_pr_name = input('Enter old number of the project: ')
        new_pr_name = input('Enter new number of the project: ')
        # make new list with new file names with help of re module
        output_files_list = [re.sub(old_pr_name, new_pr_name, file_name) for file_name in input_files_list]
        print(f'{SEPARATOR}\nNew file names for files *.{file_ext} are:\n')
        for number in range(len(output_files_list)):
            print(output_files_list[number])
        if input(f'{SEPARATOR}\nRename? (yes/no): ') in ('yes', 'Yes', 'YES', 'y', "Y"):
            # rename files if user agree with new file names
            for number in range(len(input_files_list)):
                old_full_name = path.join(os.getcwd(), input_files_list[number])
                new_full_name = path.join(os.getcwd(), output_files_list[number])
                os.rename(old_full_name, new_full_name)
        else:
            print(f'{SEPARATOR}\nRename operation canceled.')
    else:
        print(f'{SEPARATOR}\nThere are not files *.{file_ext} in current directory')


rename_files('idw')

input(f'{SEPARATOR}\nTask is finished.\n\nPress ENTER')
