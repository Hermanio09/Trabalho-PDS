import tkinter as tk
from login_cadastro import LoginView
from banca import ProfessorController

if __name__ == "__main__":
    controller = ProfessorController()
    login_view = LoginView(tk.Tk(), controller)
    login_view.root.mainloop()
