import tkinter as tk
import subprocess
from tkinter import filedialog
from tkinter import *

def run_selected_script():
    if var.get() == 1:
        subprocess.call(["python", "ArcGIS.py"])
    elif var.get() == 2:
        subprocess.call(["python", "QGIS.py"])
    elif var.get() == 3:
        subprocess.call(["python", "CSV_Converter.py"])

    root.destroy()

root = tk.Tk()
root.title("Select Script to Run")
var = tk.IntVar()
root.geometry("455x233")

text_size = 12
font_style = ("Arial", text_size)

Label(root, text='GIS-SWMM-GIS Conversion Toolbox',justify=LEFT, padx=10, pady=10,font=font_style).pack()

radio_ArcGIS = tk.Radiobutton(root, text="ArcGIS File",padx=10, pady=7, variable=var, value=1,font=font_style)
radio_QGIS = tk.Radiobutton(root, text="QGIS File",padx=10, pady=7, variable=var, value=2,font=font_style)
radio_CSV = tk.Radiobutton(root, text="CSV Writer",padx=10, pady=7, variable=var, value=3,font=font_style)

button_run = tk.Button(root, text="Run Selected Script",padx=10, pady=7, command=run_selected_script,font=font_style)

radio_ArcGIS.pack(anchor="w")
radio_QGIS.pack(anchor="w")
radio_CSV.pack(anchor="w")
button_run.pack()

root.file_dialog = tk.Toplevel(root)
root.file_dialog.withdraw()

root.mainloop()
