import os
import platform
import time

# Global variables
INPUT_FILENAME = "OK!ZEIT_1_Ausgangsdaten.txt"
OUTPUT_FILENAME1 = "OK!ZEIT_2_Allgemeine_Zeit.txt"
OUTPUT_FILENAME2 = "OK!ZEIT_3_Projekte_Zeit.txt"
YEAR = "2024"

messages = {
    'create file': f'Create a file "{INPUT_FILENAME}" and copy your data there.\n'
                   'If the file is created, press Enter to begin processing the data.',
    'enter year': f'Enter the year the table was filled in (default value is "{YEAR}"),\n'
                  'and press Enter to continue.'
}


def clear_screen(timeout=0):
    time.sleep(timeout)
    if platform.system() == 'Linux':
        os.system('clear')
    else:
        os.system('cls')


def show_message(message, default=None):
    clear_screen()
    print(message)
    answer = input("==> ")
    if not answer:
        answer = default
    clear_screen()
    return answer


show_message(messages['create file'])

YEAR = show_message(messages['enter year'], YEAR)

# Open the input file for reading
with open(INPUT_FILENAME, "r") as file:
    lines = file.readlines()

new_line = []
count = True
eingang = True
line_number = 1
first_line = ("Start Date", "Start Time", "End Date", "End Time", "Duration")
# Open a new file for writing
with open(OUTPUT_FILENAME1, "w") as file1:
    # Write first line
    file1.write("\t".join(first_line) + "\n")
    line_number += 1
    # Iterate through the lines in the original file
    for line in reversed(lines):
        if line != "\n":
            if line in ("Eingang\n",):
                count = True
                eingang = True
            elif line in ("Starte\n", "Unterbreche\n"):
                count = False
            elif line in ("Ausgang\n",):
                count = True
                eingang = False
            elif line[2] is ".":
                if count:
                    new_line.append(line[0:6] + YEAR)
                    new_line.append(line[7:12])
                    if not eingang:
                        new_line.append(f"=D{line_number}-B{line_number}")
                        file1.write("\t".join(new_line) + "\n")
                        line_number += 1
                        new_line = []
    file1.write("\t" * (len(first_line)-1) + f"=SUM(E2:E{line_number - 1})\n")


new_line2 = []
count = True
starte = False
line_number = 1
first_line = ("Start Date", "Start Time", "Project", "End Date", "End Time", "Duration")
# Open a new file for writing
with open(OUTPUT_FILENAME2, "w") as file2:
    # Write first line
    file2.write("\t".join(first_line) + "\n")
    line_number += 1
    # Iterate through the lines in the original file
    for line in reversed(lines):
        if line != "\n":
            if line in ("Starte\n",):
                count = True
                starte = True
            elif ": " in line and starte:
                new_line2.append(line[0:-1])
            elif line in ("Eingang\n", "Ausgang\n"):
                count = False
            elif line in ("Unterbreche\n",):
                count = True
                starte = False
            elif line[2] is ".":
                if count:
                    new_line2.append(line[0:6] + YEAR)
                    new_line2.append(line[7:12])
                    if not starte:
                        new_line2.append(f"=E{line_number}-B{line_number}")
                        file2.write("\t".join(new_line2) + "\n")
                        line_number += 1
                        new_line2 = []
    file2.write("\t" * (len(first_line)-1) + f"=SUM(F2:F{line_number - 1})\n")
