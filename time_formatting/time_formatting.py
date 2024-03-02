import os
import platform
import time
import tkinter as tk
from tkinter import filedialog


def clear_screen(timeout=0):
    time.sleep(timeout)
    if platform.system() == 'Linux':
        os.system('clear')
    else:
        os.system('cls')


def process_data():
    clear_screen()
    year = year_entry.get() or "2024"

    filename = filedialog.askopenfilename(title="Select File", filetypes=[("Text files", "*.txt")])
    if not filename:
        return

    # Open the original file for reading
    with open(filename, "r") as file:
        lines = file.readlines()

    # Open a new file for writing
    output_filename = "formatted.txt"
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


# Create GUI
root = tk.Tk()
root.title("Data Formatter")

year_label = tk.Label(root, text="Enter the year:")
year_label.pack()

year_entry = tk.Entry(root)
year_entry.pack()

process_button = tk.Button(root, text="Process Data", command=process_data)
process_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
