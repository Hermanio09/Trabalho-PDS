import tkinter as tk
from tkinter import messagebox


class BancaView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Sistema de Cadastro de Bancas de TCC")
        self.root.geometry("400x500")

        # Widgets para cadastro de banca
        tk.Label(self.root, text="Nome do Aluno:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.aluno_entry = tk.Entry(self.root, width=40)
        self.aluno_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Nome do Orientador:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.orientador_entry = tk.Entry(self.root, width=40)
        self.orientador_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Título:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.titulo_entry = tk.Entry(self.root, width=40)
        self.titulo_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Data (AAAA-MM-DD):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.data_entry = tk.Entry(self.root, width=40)
        self.data_entry.grid(row=3, column=1, padx=10, pady=5)

        self.cadastrar_button = tk.Button(self.root, text="Cadastrar", command=self.cadastrar_banca)
        self.cadastrar_button.grid(row=4, column=0, columnspan=2, pady=10)

        tk.Label(self.root, text="Buscar:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.busca_entry = tk.Entry(self.root, width=40)
        self.busca_entry.grid(row=5, column=1, padx=10, pady=5)

        self.buscar_button = tk.Button(self.root, text="Buscar", command=self.buscar_bancas)
        self.buscar_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.lista_bancas = tk.Listbox(self.root, width=60, height=15)
        self.lista_bancas.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.remover_button = tk.Button(self.root, text="Remover Banca", command=self.remover_banca)
        self.remover_button.grid(row=8, column=0, pady=10)

        self.editar_button = tk.Button(self.root, text="Editar Banca", command=self.editar_banca)
        self.editar_button.grid(row=8, column=1, pady=10)

    def cadastrar_banca(self):
        aluno = self.aluno_entry.get()
        orientador = self.orientador_entry.get()
        titulo = self.titulo_entry.get()
        data = self.data_entry.get()

        if not aluno or not orientador or not titulo or not data:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        self.controller.adicionar_banca(aluno, orientador, titulo, data)
        messagebox.showinfo("Sucesso", "Banca cadastrada com sucesso!")
        self.atualizar_lista()

    def buscar_bancas(self):
        termo = self.busca_entry.get()
        bancas = self.controller.buscar_bancas(termo)
        self.lista_bancas.delete(0, tk.END)
        for banca in bancas:
            self.lista_bancas.insert(tk.END, f"{banca['aluno_nome']} - {banca['titulo']}")

    def remover_banca(self):
        selecionado = self.lista_bancas.curselection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione uma banca para remover!")
            return

        index = selecionado[0]
        self.controller.remover_banca(index)
        messagebox.showinfo("Sucesso", "Banca removida com sucesso!")
        self.atualizar_lista()

    def editar_banca(self):
        selecionado = self.lista_bancas.curselection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione uma banca para editar!")
            return

        index = selecionado[0]
        bancas = self.controller.get_bancas()
        banca = bancas[index]

        # Preenche os campos de entrada com os dados da banca
        self.aluno_entry.delete(0, tk.END)
        self.aluno_entry.insert(0, banca["aluno_nome"])

        self.orientador_entry.delete(0, tk.END)
        self.orientador_entry.insert(0, banca["orientador_nome"])

        self.titulo_entry.delete(0, tk.END)
        self.titulo_entry.insert(0, banca["titulo"])

        self.data_entry.delete(0, tk.END)
        self.data_entry.insert(0, banca["data"])

        # Substitui o botão de cadastro por um botão de salvar edição
        self.cadastrar_button.config(text="Salvar Alterações", command=lambda: self.salvar_edicao(index))

    def salvar_edicao(self, index):
        aluno = self.aluno_entry.get()
        orientador = self.orientador_entry.get()
        titulo = self.titulo_entry.get()
        data = self.data_entry.get()

        if not aluno or not orientador or not titulo or not data:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        self.controller.editar_banca(index, aluno, orientador, titulo, data)
        messagebox.showinfo("Sucesso", "Banca editada com sucesso!")
        self.atualizar_lista()

        # Restaura o botão de cadastro
        self.cadastrar_button.config(text="Cadastrar", command=self.cadastrar_banca)

    def atualizar_lista(self):
        self.lista_bancas.delete(0, tk.END)
        bancas = self.controller.get_bancas()
        for banca in bancas:
            self.lista_bancas.insert(tk.END, f"{banca['aluno_nome']} - {banca['titulo']}")


class ProfessorController:
    def __init__(self):
        self.bancas = []

    def adicionar_banca(self, aluno_nome, orientador_nome, titulo, data):
        self.bancas.append({"aluno_nome": aluno_nome, "orientador_nome": orientador_nome, "titulo": titulo, "data": data})

    def buscar_bancas(self, termo):
        return [banca for banca in self.bancas if termo.lower() in banca["aluno_nome"].lower() or termo.lower() in banca["titulo"].lower()]

    def remover_banca(self, index):
        if 0 <= index < len(self.bancas):
            del self.bancas[index]

    def editar_banca(self, index, aluno_nome, orientador_nome, titulo, data):
        if 0 <= index < len(self.bancas):
            self.bancas[index] = {"aluno_nome": aluno_nome, "orientador_nome": orientador_nome, "titulo": titulo, "data": data}

    def get_bancas(self):
        return self.bancas


if __name__ == "__main__":
    root = tk.Tk()
    controller = ProfessorController()
    app = BancaView(root, controller)
    root.mainloop()
