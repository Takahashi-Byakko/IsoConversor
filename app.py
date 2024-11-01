import os
import rarfile
import shutil
import tkinter as tk
from tkinter import filedialog
from pycdlib import PyCdlib

def select_rar_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("RAR files", "*.rar"), ("All Files", "*.*")]
    )
    if filepath:
        rar_file_path.set(filepath)

def select_output_iso():
    filepath = filedialog.asksaveasfilename(defaultextension=".iso", filetypes=[("ISO files", "*.iso")])
    if filepath:
        iso_output_path.set(filepath)

def sanitize_iso_filename(filename):
    # Mantém apenas caracteres A-Z, 0-9, e substitui outros por '_'
    return ''.join(c if c.isalnum() else '_' for c in filename).upper()

def convert_rar_to_iso():
    rar_path = rar_file_path.get()
    iso_path = iso_output_path.get()
    temp_dir = "temp_extracted_files"

    try:
        # Extrair o arquivo RAR
        with rarfile.RarFile(rar_path) as rf:
            rf.extractall(temp_dir)

        # Criar o arquivo ISO
        iso = PyCdlib()
        iso.new(interchange_level=3)
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                iso_path_in_iso = os.path.relpath(file_path, temp_dir)
                sanitized_name = sanitize_iso_filename(iso_path_in_iso)
                iso.add_file(file_path, f'/{sanitized_name};1')
        iso.write(iso_path)
        iso.close()

        # Limpeza
        shutil.rmtree(temp_dir)
        status_label.config(text="Conversão concluída!")
    except rarfile.NotRarFile:
        status_label.config(text="Erro: Selecione um arquivo.rar")

# Configuração da Interface Gráfica
app = tk.Tk()
app.title("Conversor de RAR para ISO")
app.geometry("400x150")  # Largura x Altura

rar_file_path = tk.StringVar()
iso_output_path = tk.StringVar()

# Layout dos componentes da GUI
tk.Label(app, text="Arquivo RAR:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=rar_file_path, width=30).grid(row=0, column=1)
tk.Button(app, text="Procurar", command=select_rar_file).grid(row=0, column=2, padx=10)

tk.Label(app, text="Salvar ISO como:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(app, textvariable=iso_output_path, width=30).grid(row=1, column=1)
tk.Button(app, text="Procurar", command=select_output_iso).grid(row=1, column=2, padx=10)

tk.Button(app, text="Converter", command=convert_rar_to_iso).grid(row=2, column=1, pady=5)

# Label para exibir o status
status_label = tk.Label(app, text="")
status_label.grid(row=3, column=1, pady=10)

app.mainloop()