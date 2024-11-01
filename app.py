import os
import rarfile
import shutil
import tkinter as tk
from tkinter import filedialog
from pycdlib import PyCdlib

def select_rar_file():
    filepath = filedialog.askopenfilename(filetypes=[("RAR files", "*.rar")])
    if filepath:
        rar_file_path.set(filepath)

def select_output_iso():
    filepath = filedialog.asksaveasfilename(defaultextension=".iso", filetypes=[("ISO files", "*.iso")])
    if filepath:
        iso_output_path.set(filepath)

def convert_rar_to_iso():
    rar_path = rar_file_path.get()
    iso_path = iso_output_path.get()
    temp_dir = "temp_extracted_files"

    # Extract RAR file
    with rarfile.RarFile(rar_path) as rf:
        rf.extractall(temp_dir)

    # Create ISO
    iso = PyCdlib()
    iso.new(interchange_level=3)
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            iso_path_in_iso = os.path.relpath(file_path, temp_dir)
            iso.add_file(file_path, f'/{iso_path_in_iso.upper()};1')
    iso.write(iso_path)
    iso.close()

    # Cleanup
    shutil.rmtree(temp_dir)
    print("Conversão concluída! ISO salvo em:", iso_path)

# GUI Setup
app = tk.Tk()
app.title("Conversor de RAR para ISO")

rar_file_path = tk.StringVar()
iso_output_path = tk.StringVar()

tk.Label(app, text="Arquivo RAR:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=rar_file_path, width=40).grid(row=0, column=1)
tk.Button(app, text="Procurar", command=select_rar_file).grid(row=0, column=2, padx=10)

tk.Label(app, text="Salvar ISO como:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=iso_output_path, width=40).grid(row=1, column=1)
tk.Button(app, text="Procurar", command=select_output_iso).grid(row=1, column=2, padx=10)

tk.Button(app, text="Converter", command=convert_rar_to_iso).grid(row=2, column=1, pady=20)

app.mainloop()
