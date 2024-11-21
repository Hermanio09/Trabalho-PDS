import json
import os
import tkinter as tk
from tkinter import messagebox
from views.components import criar_label, criar_entry  # Certifique-se de ter esses módulos implementados.

class BancaModel:
    DATA_FILE = "bancas.json"

    @staticmethod
    def carregar_dados():
        """Carrega as bancas do arquivo JSON. Retorna uma lista vazia se o arquivo não existir."""
        if not os.path.exists(BancaModel.DATA_FILE):
            return []
        try:
            with open(BancaModel.DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []  # Retorna uma lista vazia em caso de arquivo corrompido.

    @staticmethod
    def salvar_dados(bancas):
        """Salva a lista de bancas no arquivo JSON."""
        try:
            with open(BancaModel.DATA_FILE, "w") as file:
                json.dump(bancas, file, indent=4)
        except IOError as e:
            print(f"Erro ao salvar dados: {e}")

    @staticmethod
    def adicionar_banca(aluno_nome, orientador_nome, titulo, data):
        """Adiciona uma nova banca à lista e salva no arquivo."""
        bancas = BancaModel.carregar_dados()
        banca = {
            "aluno_nome": aluno_nome,
            "orientador_nome": orientador_nome,
            "titulo": titulo,
            "data": data,
        }
        bancas.append(banca)
        BancaModel.salvar_dados(bancas)

    @staticmethod
    def editar_banca(index, aluno_nome, orientador_nome, titulo, data):
        """Edita uma banca existente na lista."""
        bancas = BancaModel.carregar_dados()
        if 0 <= index < len(bancas):
            bancas[index] = {
                "aluno_nome": aluno_nome,
                "orientador_nome": orientador_nome,
                "titulo": titulo,
                "data": data,
            }
            BancaModel.salvar_dados(bancas)

    @staticmethod
    def remover_banca(index):
        """Remove uma banca da lista pelo índice."""
        bancas = BancaModel.carregar_dados()
        if 0 <= index < len(bancas):
            bancas.pop(index)
            BancaModel.salvar_dados(bancas)

    @staticmethod
    def listar_bancas():
        """Retorna a lista de bancas."""
        return BancaModel.carregar_dados()


class CadastroProfessorView:
    def __init__(self, parent, controller):
        """Cria uma janela de cadastro de professores."""
        self.parent = parent
        self.controller = controller
        self.cadastro_professor_tela = tk.Toplevel(parent)
        self.cadastro_professor_tela.title("Cadastro de Professores")
        self.cadastro_professor_tela.geometry("300x200")

        # Elementos da interface
        criar_label(self.cadastro_professor_tela, "SIAPE:", 0, 0)
        self.siape_entry = criar_entry(self.cadastro_professor_tela, 0, 1)

        criar_label(self.cadastro_professor_tela, "Nome:", 1, 0)
        self.nome_entry = criar_entry(self.cadastro_professor_tela, 1, 1)

        criar_label(self.cadastro_professor_tela, "Senha:", 2, 0)
        self.senha_entry = criar_entry(self.cadastro_professor_tela, 2, 1)

        # Botão de cadastro
        btn_cadastrar = tk.Button(
            self.cadastro_professor_tela,
            text="Cadastrar",
            command=self.cadastrar_professor,
        )
        btn_cadastrar.grid(row=3, columnspan=2, pady=10)

    def cadastrar_professor(self):
        """Valida e cadastra o professor."""
        siape = self.siape_entry.get()
        nome = self.nome_entry.get()
        senha = self.senha_entry.get()

        # Validação de entrada
        if not siape or not nome or not senha:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        if not siape.isdigit():
            messagebox.showerror("Erro", "O SIAPE deve conter apenas números.")
            return

        # Realiza o cadastro
        try:
            self.controller.cadastrar_professor(siape, nome, senha)
            messagebox.showinfo("Sucesso", "Professor cadastrado com sucesso!")
            self.cadastro_professor_tela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar professor: {e}")
