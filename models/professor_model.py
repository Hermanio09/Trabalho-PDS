import json
import os

class ProfessorModel:
    DATA_FILE = "professores.json"

    @staticmethod
    def carregar_dados():
        """Carrega os dados dos professores do arquivo JSON. Retorna uma lista vazia se o arquivo não existir."""
        if not os.path.exists(ProfessorModel.DATA_FILE):
            return []
        with open(ProfessorModel.DATA_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def salvar_dados(professores):
        """Salva a lista de professores no arquivo JSON."""
        with open(ProfessorModel.DATA_FILE, "w") as f:
            json.dump(professores, f, indent=4)

    @staticmethod
    def cadastrar_professor(siape, nome, senha):
        """Cadastra um novo professor, evitando duplicatas pelo SIAPE."""
        professores = ProfessorModel.carregar_dados()
        if any(professor["siape"] == siape for professor in professores):
            raise ValueError("Já existe um professor cadastrado com esse SIAPE.")
        professor = {
            "siape": siape,
            "nome": nome,
            "senha": senha  # Em um sistema real, essa senha deveria ser criptografada
        }
        professores.append(professor)
        ProfessorModel.salvar_dados(professores)

    @staticmethod
    def autenticar_professor(siape, senha):
        """Verifica se o SIAPE e a senha correspondem a um professor cadastrado."""
        professores = ProfessorModel.carregar_dados()
        for professor in professores:
            if professor["siape"] == siape and professor["senha"] == senha:
                return True
        return False
