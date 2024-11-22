import tkinter as tk
from login_cadastro import LoginCadastroView
from controllers.usuario_controller import UsuarioController

if __name__ == "__main__":
    usuario_controller = UsuarioController()

    root = tk.Tk()
    app = LoginCadastroView(root, usuario_controller)

    root.mainloop()
