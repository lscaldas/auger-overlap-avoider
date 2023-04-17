#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import tkinter.font as tkfont

# Function to handle button click event
def process_elements():
    elements = elements_entry.get().split(',')
    elements = [elem.strip() for elem in elements]

    limit = int(limit_entry.get())
    lower_ke = int(lower_ke_entry.get())
    upper_ke = int(upper_ke_entry.get())
    sensitivity = float(sensitivity_entry.get())

    af = pd.read_csv('auger_energies_coghlan_clausing.csv')
    af2 = af[(af['ele'].isin(elements)) & (af['ener'] >= lower_ke) & (af['ener'] < upper_ke) & (af['cs'] >= sensitivity)]

    forb_ke = []

    for index, row in af2.iterrows():
        fb = list(range(row['ener'] - limit, row['ener'] + 10))
        forb_ke.extend(fb)

    af2 = af2.reset_index(drop=True)
    af3 = af2
    af3['cs'] = af3['cs'].round(3)  # Round 'cs' column to 3 decimal places
    af3 = af3.sort_values(by='ener')  # Sort af3 by 'ener' column in ascending order
    af3.to_csv('auger_peaks.csv', index=False)

    forb_ke = sorted(set(forb_ke))
    allowed_ke = [ke for ke in range(lower_ke, upper_ke) if ke not in forb_ke]

    new_list = []
    start = None
    end = None

    for i in range(len(allowed_ke)):
        if start is None:
            start = allowed_ke[i]
        elif allowed_ke[i] - allowed_ke[i - 1] > 1:
            end = allowed_ke[i - 1]
            new_list.append((start, end))
            start = allowed_ke[i]
            end = None
    if start is not None:
        new_list.append((start, allowed_ke[-1]))

    # Clear the output boxes
    allowed_output_tree.delete(*allowed_output_tree.get_children())
    auger_peaks_table.delete(*auger_peaks_table.get_children())

    # Display the allowed K.E. ranges in the allowed_output_tree
    for rng in new_list:
        allowed_output_tree.insert('', tk.END, values=(f"{rng[0]}-{rng[1]}",))
        
    # Display the values that go into the auger_peaks.csv file in the auger_peaks_table
    for _, row in af3.iterrows():
        auger_peaks_table.insert('', tk.END, values=(row['Z'], row['ele'], row['trans_type'], row['ener'], row['cs'], row['line_disp'], row['bind_ener']))

    # Resize treeview columns to match heading length
    for col in auger_peaks_table['columns']:
        heading_width = len(auger_peaks_table.heading(col)['text']) * 8
        auger_peaks_table.column(col, width=heading_width)


# Create ThemedTk application window
root = ThemedTk(theme="clearlooks")
#clearlooks
#radiance

def resize_root():
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    root.geometry(f"{width}x{height}+{x}+{y}")


root.after(100, resize_root)

root.title("Auger Overlap Avoider v.13 by L.S.Caldas")

# Create a main frame to hold all the widgets
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(expand=True, fill=tk.BOTH)

# Create input frame to hold all the input widgets
input_frame = ttk.Frame(main_frame, padding="20")
input_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W+tk.E)

# Create label and entry for elements
elements_label = ttk.Label(input_frame, text="Insert the elements present in your sample (comma-separated):")
elements_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
elements_entry = ttk.Entry(input_frame, width=60)
elements_entry.insert(0, "C,O")
elements_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

# Create a label with the description of the code
label_text = "Auger Overlap Avoider v.13\n\n"              "Created by Lucas de Souza Caldas.\n\n"              "Database by W.A. Coghlan, and R.E. Clausing.\n\n"              "Each time the OK button is pressed, an excel .csv\n  file is created(or replaced) with the auger_peaks.\n\n"              "Press OK to show the allowed Kinetic energy ranges,\n  and the Auger peaks inside the K.E. boundaries selected.\n"
label = ttk.Label(main_frame, text=label_text, justify=tk.RIGHT, padding="10")
label.grid(row=0, column=1, padx=20, pady=20, sticky=tk.E+tk.N)

# Create label and entry for limit
limit_label = ttk.Label(input_frame, text="Distance from any Auger peaks (default: 10 eV):")
limit_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
limit_entry = ttk.Entry(input_frame)
limit_entry.insert(0, "10")
limit_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

# Create label and entry for lower_ke
lower_ke_label = ttk.Label(input_frame, text="Lower kinetic energy (default: 50 eV):")
lower_ke_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
lower_ke_entry = ttk.Entry(input_frame)
lower_ke_entry.insert(0, "50")
lower_ke_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

# Create label and entry for upper_ke
upper_ke_label = ttk.Label(input_frame, text="Upper kinetic energy (default: 1200 eV):")
upper_ke_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
upper_ke_entry = ttk.Entry(input_frame)
upper_ke_entry.insert(0, "1200")
upper_ke_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

# Create label and entry for sensitivity
sensitivity_label = ttk.Label(input_frame, text="Lower cross section limit (default: 0.05):")
sensitivity_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
sensitivity_entry = ttk.Entry(input_frame)
sensitivity_entry.insert(0, "0.05")
sensitivity_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

# Create a ttk.Style object
style = ttk.Style(root)

# Create button to process elements
custom_font = tkfont.Font(family="Helvetica", size=16, weight="normal") 
style.configure("Custom.TButton", font=custom_font)

# Create button to process elements
process_button = ttk.Button(main_frame, text="OK", command=process_elements, style="Custom.TButton")
process_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

# Create output boxes
output_frame = ttk.Frame(main_frame, padding="20")
output_frame.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)

# Convert allowed_output_box into a treeview object
allowed_output_tree = ttk.Treeview(output_frame, columns=("allowed_ke",), show="headings", height=20)
allowed_output_tree.pack(side="left", padx=(0, 0))
allowed_output_tree.heading("allowed_ke", text="Allowed K.E.")
allowed_output_tree.column("allowed_ke", width=100, anchor="center")

# Adding a scrollbar to the allowed_output_tree
allowed_scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=allowed_output_tree.yview)
allowed_scrollbar.pack(side="left", fill="y")
allowed_output_tree.configure(yscrollcommand=allowed_scrollbar.set)

# Create a Treeview for the auger_peaks table
auger_peaks_table = ttk.Treeview(output_frame, columns=("Z", "ele", "trans_type", "ener", "cs", "line_disp", "bind_ener"), show="headings", height=10)
auger_peaks_table.pack(side="left", padx=(20, 0), fill=tk.BOTH, expand=True)
auger_peaks_table.heading("Z", text="Z")
auger_peaks_table.heading("ele", text="Element")
auger_peaks_table.heading("trans_type", text="Transition")
auger_peaks_table.heading("ener", text="Auger K.E. (eV)")
auger_peaks_table.heading("cs", text="Cross Section")
auger_peaks_table.heading("line_disp", text="Core level")
auger_peaks_table.heading("bind_ener", text="Core level B.E. (eV)")

# Resize the columns
for col in auger_peaks_table['columns']:
    auger_peaks_table.column(col, anchor="center", width=len(auger_peaks_table.heading(col)['text']) * 10)

# Adding a scrollbar to the auger_peaks table
scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=auger_peaks_table.yview)
scrollbar.pack(side="right", fill="y")
auger_peaks_table.configure(yscrollcommand=scrollbar.set)

root.mainloop()

