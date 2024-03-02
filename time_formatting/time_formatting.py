import os
import platform
import time
import tkinter as tk
from tkinter import filedialog

# Global variable to store the input file name
input_filename = ""


def clear_screen(timeout=0):
    time.sleep(timeout)
    if platform.system() == 'Linux':
        os.system('clear')
    else:
        os.system('cls')


def process_data():
    global input_filename  # Zugriff auf die globale Variable
    clear_screen()
    year = year_entry.get() or "2024"

    input_filename = filedialog.askopenfilename(title="Select Input File", filetypes=[("Text files", "*.txt")])
    if not input_filename:
        return

    output_dir = os.path.dirname(input_filename)
    output_filename = os.path.join(output_dir, "formatted.txt")

    # Open the original file for reading
    with open(input_filename, "r") as file:
        lines = file.readlines()

    # Open a new file for writing
    with open(output_filename, "w") as file:
        # Write first line
        file.write("Date\tStart Time\tDuration\tProject Code\n")
        # Iterate through the lines in the original file
        row = 1
        for i in range(0, len(lines), 4):
            # Extract information from four consecutive lines
            date = lines[i].strip()
            formatted_date = date[:6] + year
            time_str = date[6:]
            duration = lines[i + 1].strip()
            code = lines[i + 3].strip()

            # Write the formatted line to the new file
            file.write(f"{formatted_date}\t{time_str}\t{duration}\t{code}\n")
            row += 1
        file.write(f"\tTotal:\t=SUM(C2:C{str(row)})")

    clear_screen()
    result_label.config(text=f"Formatted data saved in {output_filename}")


def open_formatted_file():
    global input_filename  # Zugriff auf die globale Variable
    output_filename = os.path.join(os.path.dirname(input_filename), "formatted.txt")
    if os.path.exists(output_filename):
        os.system(f'start "" "{output_filename}"')
    else:
        result_label.config(text="Formatted file not found!")


# Create GUI
root = tk.Tk()
root.title("Data Formatter")
root.geometry("500x125")

year_label = tk.Label(root, text="Enter the year:")
year_label.pack()

year_entry = tk.Entry(root)
year_entry.pack()

process_button = tk.Button(root, text="Process Data", command=process_data)
process_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

open_button = tk.Button(root, text="Open Formatted File", command=open_formatted_file)
open_button.pack()

root.mainloop()
