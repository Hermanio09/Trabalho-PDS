import tkinter as tk
from tkinter import messagebox
from banca import ProfessorController, BancaView  # Importa o Controller e a tela de Banca

class LoginView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Tela de Login")
        self.root.geometry("400x300")
        
        # Campos de entrada para login
        tk.Label(self.root, text="SIAPE:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.siape_entry = tk.Entry(self.root, width=40)
        self.siape_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Senha:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.senha_entry = tk.Entry(self.root, width=40, show="*")
        self.senha_entry.grid(row=1, column=1, padx=10, pady=5)

        # Botões de Login e Cadastro
        self.login_button = tk.Button(self.root, text="Login", command=self.realizar_login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.cadastrar_button = tk.Button(self.root, text="Cadastrar", command=self.abrir_cadastro)
        self.cadastrar_button.grid(row=3, column=0, columnspan=2, pady=10)

    def realizar_login(self):
        siape = self.siape_entry.get()
        senha = self.senha_entry.get()

        if not siape or not senha:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        if self.controller.autenticar_professor(siape, senha):
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.root.destroy()  
            self.abrir_tela_banca()  # Abre a tela de cadastro de bancas
        else:
            messagebox.showerror("Erro", "SIAPE ou senha incorretos!")

    def abrir_cadastro(self):
        self.root.destroy()
        cadastro_view = CadastroView(tk.Tk(), self.controller)  # Abre a tela de cadastro
        cadastro_view.root.mainloop()

    def abrir_tela_banca(self):
        janela_banca = tk.Tk()
        banca_view = BancaView(janela_banca, self.controller)  # Passa o controller para a tela de bancas
        janela_banca.mainloop()

class CadastroView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Tela de Cadastro")
        self.root.geometry("400x300")
        
        tk.Label(self.root, text="SIAPE:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.siape_entry = tk.Entry(self.root, width=40)
        self.siape_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Senha:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.senha_entry = tk.Entry(self.root, width=40, show="*")
        self.senha_entry.grid(row=1, column=1, padx=10, pady=5)

        self.cadastrar_button = tk.Button(self.root, text="Cadastrar", command=self.realizar_cadastro)
        self.cadastrar_button.grid(row=2, column=0, columnspan=2, pady=10)

    def realizar_cadastro(self):
        siape = self.siape_entry.get()
        senha = self.senha_entry.get()

        if not siape or not senha:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        if self.controller.existe_professor(siape):
            messagebox.showerror("Erro", "SIAPE já cadastrado!")
            return

        self.controller.cadastrar_professor(siape, senha)
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
        self.root.destroy()
        login_view = LoginView(tk.Tk(), self.controller)  
        login_view.root.mainloop()

# Inicia a aplicação
if __name__ == "__main__":
    controller = ProfessorController()
    login_view = LoginView(tk.Tk(), controller)
    login_view.root.mainloop()
