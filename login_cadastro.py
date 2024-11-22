import tkinter as tk
from tkinter import messagebox
from controllers.usuario_controller import UsuarioController
from banca import ProfessorController, BancaView

class LoginCadastroView:
    def __init__(self, root, usuario_controller):
        """
        Inicializa a interface de login e cadastro.
        """
        self.root = root
        self.root.title("Login e Cadastro de Usuários")
        self.usuario_controller = usuario_controller

        # Widgets para login
        tk.Label(root, text="Email:").grid(row=0, column=0, pady=5)
        self.email_entry = tk.Entry(root, width=30)
        self.email_entry.grid(row=0, column=1)

        tk.Label(root, text="Senha:").grid(row=1, column=0, pady=5)
        self.senha_entry = tk.Entry(root, show="*", width=30)
        self.senha_entry.grid(row=1, column=1)

        # Botões
        tk.Button(root, text="Login", command=self.realizar_login, width=15).grid(row=2, column=0, pady=10)
        tk.Button(root, text="Cadastrar", command=self.abrir_tela_cadastro, width=15).grid(row=2, column=1, pady=10)

    def realizar_login(self):
        """
        Realiza a autenticação do usuário.
        """
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        if email and senha:
            autenticado = self.usuario_controller.autenticar_usuario(email, senha)
            if autenticado:
                messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
                self.abrir_tela_banca()  # Redireciona para a tela de cadastro de banca
            else:
                messagebox.showerror("Erro", "Email ou senha inválidos!")
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos!")

    def abrir_tela_banca(self):
        """
        Abre a tela de cadastro de banca após o login.
        """
        banca_window = tk.Toplevel(self.root)  # Cria uma nova janela
        banca_controller = ProfessorController()  # Criando o controller para a banca
        BancaView(banca_window, banca_controller)  # Passa a nova janela e o controller para a BancaView

    def abrir_tela_cadastro(self):
        """
        Abre uma nova janela para cadastro de usuários.
        """
        cadastro_window = tk.Toplevel(self.root)
        cadastro_window.title("Cadastro de Usuário")

        tk.Label(cadastro_window, text="Nome:").grid(row=0, column=0, pady=5)
        nome_entry = tk.Entry(cadastro_window, width=30)
        nome_entry.grid(row=0, column=1)

        tk.Label(cadastro_window, text="Email:").grid(row=1, column=0, pady=5)
        email_entry = tk.Entry(cadastro_window, width=30)
        email_entry.grid(row=1, column=1)

        tk.Label(cadastro_window, text="Senha:").grid(row=2, column=0, pady=5)
        senha_entry = tk.Entry(cadastro_window, show="*", width=30)
        senha_entry.grid(row=2, column=1)

        def cadastrar_usuario():
            """
            Registra um novo usuário.
            """
            nome = nome_entry.get()
            email = email_entry.get()
            senha = senha_entry.get()

            if nome and email and senha:
                mensagem = self.usuario_controller.cadastrar_usuario(nome, email, senha)
                messagebox.showinfo("Cadastro", mensagem)
                cadastro_window.destroy()
            else:
                messagebox.showwarning("Erro", "Preencha todos os campos!")

        tk.Button(cadastro_window, text="Cadastrar", command=cadastrar_usuario, width=15).grid(row=3, column=0, columnspan=2, pady=10)
