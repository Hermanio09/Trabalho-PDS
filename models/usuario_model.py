import json
import os


class UsuarioModel:
    def __init__(self, arquivo_dados="usuarios.json"):
        self.arquivo_dados = arquivo_dados
        self.usuarios = self.carregar_dados()

    def carregar_dados(self):
        """Carrega os dados dos usuários do arquivo JSON."""
        if os.path.exists(self.arquivo_dados):
            with open(self.arquivo_dados, "r") as arquivo:
                return json.load(arquivo)
        return []

    def salvar_dados(self):
        """Salva os dados dos usuários no arquivo JSON."""
        with open(self.arquivo_dados, "w") as arquivo:
            json.dump(self.usuarios, arquivo, indent=4)

    def adicionar_usuario(self, nome, email, senha):
        """Adiciona um novo usuário ao sistema."""
        for usuario in self.usuarios:
            if usuario["email"] == email:
                return "Erro: Email já cadastrado."

        novo_usuario = {"nome": nome, "email": email, "senha": senha}
        self.usuarios.append(novo_usuario)
        self.salvar_dados()
        return "Usuário cadastrado com sucesso."

    def autenticar_usuario(self, email, senha):
        """Autentica um usuário pelo email e senha."""
        for usuario in self.usuarios:
            if usuario["email"] == email and usuario["senha"] == senha:
                return True
        return False
