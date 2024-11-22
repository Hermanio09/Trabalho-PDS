from models.usuario_model import UsuarioModel


class UsuarioController:
    def __init__(self):
        """Inicializa o modelo de usuários."""
        self.usuario_model = UsuarioModel()

    def cadastrar_usuario(self, nome, email, senha):
        """Registra um novo usuário."""
        return self.usuario_model.adicionar_usuario(nome, email, senha)

    def autenticar_usuario(self, email, senha):
        """Autentica um usuário pelo email e senha."""
        return self.usuario_model.autenticar_usuario(email, senha)
