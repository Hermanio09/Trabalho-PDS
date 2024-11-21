import tkinter as tk
from tkinter import messagebox, simpledialog
from controllers.banca_controller import BancaController
from views.components import criar_label, criar_entry
import csv
import re
import json
import os


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Cadastro de Bancas de TCC")
        self.geometry("400x400")
        self.controller = BancaController()

        # Campos de entrada
        criar_label(self, "Nome do Aluno:", 0, 0)
        self.entry_aluno = criar_entry(self, 0, 1)

        criar_label(self, "Nome do Orientador:", 1, 0)
        self.entry_orientador = criar_entry(self, 1, 1)

        criar_label(self, "Título:", 2, 0)
        self.entry_titulo = criar_entry(self, 2, 1)

        criar_label(self, "Data (AAAA-MM-DD):", 3, 0)
        self.entry_data = criar_entry(self, 3, 1)

        # Botões
        btn_cadastrar = tk.Button(self, text="Cadastrar Banca", command=self.cadastrar_banca)
        btn_cadastrar.grid(row=4, columnspan=2, pady=10)

        btn_exportar = tk.Button(self, text="Exportar para CSV", command=self.exportar_para_csv)
        btn_exportar.grid(row=8, columnspan=2, pady=10)

        btn_editar = tk.Button(self, text="Editar Banca", command=self.editar_banca)
        btn_editar.grid(row=4, column=1, pady=10)

        # Área de exibição de dados
        self.lista_bancas = tk.Listbox(self)
        self.lista_bancas.grid(row=5, columnspan=2, sticky="nsew", pady=10)

        btn_remover = tk.Button(self, text="Remover Banca", command=self.remover_banca)
        btn_remover.grid(row=6, columnspan=2, pady=10)

        btn_detalhes = tk.Button(self, text="Detalhes", command=self.exibir_detalhes)
        btn_detalhes.grid(row=6, column=1, pady=10)

        btn_ordenar = tk.Button(self, text="Ordenar por Aluno", command=self.ordenar_bancas)
        btn_ordenar.grid(row=7, columnspan=2, pady=10)

        criar_label(self, "Buscar:", 4, 0)
        self.entry_busca = criar_entry(self, 4, 1)

        btn_buscar = tk.Button(self, text="Buscar", command=self.buscar_bancas)
        btn_buscar.grid(row=5, column=1, pady=10)

        btn_atribuir = tk.Button(self, text="Atribuir Avaliadores", command=self.atribuir_banca)
        btn_atribuir.grid(row=9, columnspan=2, pady=10)

        btn_nota = tk.Button(self, text="Registrar Nota", command=self.registrar_nota)
        btn_nota.grid(row=10, columnspan=2, pady=10)

        self.carregar_bancas()

    def cadastrar_banca(self):
        aluno = self.entry_aluno.get()
        orientador = self.entry_orientador.get()
        titulo = self.entry_titulo.get()
        data = self.entry_data.get()

        if self.validar_dados(aluno, orientador, titulo, data):
            self.controller.adicionar_banca(aluno, orientador, titulo, data)
            self.carregar_bancas()

    def carregar_bancas(self):
        self.lista_bancas.delete(0, tk.END)
        bancas = self.controller.obter_bancas()
        for banca in bancas:
            self.lista_bancas.insert(tk.END, f"{banca['aluno_nome']} - {banca['orientador_nome']} - {banca['titulo']} - {banca['data']}")

    def editar_banca(self):
        selected_index = self.lista_bancas.curselection()
        if selected_index:
            index = selected_index[0]
            aluno = self.entry_aluno.get()
            orientador = self.entry_orientador.get()
            titulo = self.entry_titulo.get()
            data = self.entry_data.get()
            self.controller.editar_banca(index, aluno, orientador, titulo, data)
            self.carregar_bancas()

    def remover_banca(self):
        selected_index = self.lista_bancas.curselection()
        if selected_index:
            index = selected_index[0]
            self.controller.remover_banca(index)
            self.carregar_bancas()

    def buscar_bancas(self):
        termo = self.entry_busca.get()
        bancas = self.controller.buscar_bancas(termo)
        self.lista_bancas.delete(0, tk.END)
        for banca in bancas:
            self.lista_bancas.insert(tk.END, f"{banca['aluno_nome']} - {banca['orientador_nome']} - {banca['titulo']} - {banca['data']}")

    def exibir_detalhes(self):
        selected_index = self.lista_bancas.curselection()
        if selected_index:
            index = selected_index[0]
            banca = self.controller.obter_bancas()[index]
            detalhes = (f"Nome do Aluno: {banca['aluno_nome']}\n"
                        f"Nome do Orientador: {banca['orientador_nome']}\n"
                        f"Título: {banca['titulo']}\n"
                        f"Data: {banca['data']}")
            messagebox.showinfo("Detalhes da Banca", detalhes)

    def ordenar_bancas(self):
        bancas = self.controller.ordenar_bancas_por_nome()
        self.lista_bancas.delete(0, tk.END)
        for banca in bancas:
            self.lista_bancas.insert(tk.END, f"{banca['aluno_nome']} - {banca['orientador_nome']} - {banca['titulo']} - {banca['data']}")

    def exportar_para_csv(self):
        bancas = self.controller.obter_bancas()
        with open("bancas_exportadas.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Nome do Aluno", "Nome do Orientador", "Título", "Data"])
            for banca in bancas:
                writer.writerow([banca["aluno_nome"], banca["orientador_nome"], banca["titulo"], banca["data"]])
        messagebox.showinfo("Exportação", "Bancas exportadas com sucesso para bancas_exportadas.csv.")

    def validar_dados(self, aluno, orientador, titulo, data):
        if not aluno or not orientador or not titulo or not data:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return False
        if not re.match(r"\d{4}-\d{2}-\d{2}", data):
            messagebox.showerror("Erro", "Data deve estar no formato AAAA-MM-DD.")
            return False
        return True

    def atribuir_banca(self):
        selected_index = self.lista_bancas.curselection()
        if selected_index:
            index = selected_index[0]
            siape_avaliadores = simpledialog.askstring(
                "Atribuir Avaliadores",
                "Digite os SIAPEs dos avaliadores separados por vírgula:"
            )
            if siape_avaliadores:
                avaliadores = [s.strip() for s in siape_avaliadores.split(",")]
                self.controller.atribuir_banca(index, avaliadores)
                messagebox.showinfo("Sucesso", "Avaliadores atribuídos com sucesso!")

    def registrar_nota(self):
        selected_index = self.lista_bancas.curselection()
        if selected_index:
            index = selected_index[0]
            nota = simpledialog.askfloat("Registrar Nota", "Digite a nota final:")
            if nota is not None:
                self.controller.registrar_nota(index, nota)
                messagebox.showinfo("Sucesso", "Nota registrada com sucesso!")
