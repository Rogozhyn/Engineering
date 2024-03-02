import os
import platform
import time


def clear_screen(timeout=0):
    time.sleep(timeout)
    if platform.system() == 'Linux':
        os.system('clear')
    else:
        os.system('cls')


clear_screen()
input('Create a file "original.txt" and copy your data there.\n'
      'If the file is created, press Enter to begin processing the data.')
clear_screen()

year = input('Enter the year the table was filled in (default value is "2024"): ')
if not year:
    year = "2024"

# Open the original file for reading
with open("original.txt", "r") as file:
    lines = file.readlines()

# Open a new file for writing
with open("formatted.txt", "w") as file:
    # Write first line
    file.write("Date\tStart Time\tDuration\tProject Code\n")
    # Iterate through the lines in the original file
    row = 1
    for i in range(0, len(lines), 4):
        # Extract information from four consecutive lines
        date = lines[i].strip()
        formatted_date = date[:6] + year
        time = date[6:]
        duration = lines[i + 1].strip()
        code = lines[i + 3].strip()

        # Write the formatted line to the new file
        file.write(f"{formatted_date}\t{time}\t{duration}\t{code}\n")
        row += 1
    file.write(f"\tTotal:\t=SUM(C2:C{str(row)})")

clear_screen()
input('Formatted data in a file "formatted.txt".\nTo continue, press Enter.')
