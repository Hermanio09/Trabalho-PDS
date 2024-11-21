import tkinter as tk

def criar_label(janela, texto, linha, coluna):
    label = tk.Label(janela, text=texto)
    label.grid(row=linha, column=coluna, padx=5, pady=5)
    return label

def criar_entry(janela, linha, coluna):
    entry = tk.Entry(janela)
    entry.grid(row=linha, column=coluna, padx=5, pady=5)
    return entry
