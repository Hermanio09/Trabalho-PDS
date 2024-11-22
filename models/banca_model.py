import json
import os

class BancaModel:
    DATA_FILE = "C:/Users/hermanio/Documents/banca-tcc/bancas.json"

    @staticmethod
    def garantir_diretorio():
        """Garante que o diretório onde o arquivo será salvo existe."""
        os.makedirs(os.path.dirname(BancaModel.DATA_FILE), exist_ok=True)

    @staticmethod
    def carregar_dados():
        """Carrega os dados das bancas do arquivo JSON."""
        if not os.path.exists(BancaModel.DATA_FILE):
            return []
        try:
            with open(BancaModel.DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Erro ao ler o arquivo JSON. Retornando lista vazia.")
            return []

    @staticmethod
    def salvar_dados(bancas):
        """Salva os dados das bancas no arquivo JSON."""
        try:
            BancaModel.garantir_diretorio()
            with open(BancaModel.DATA_FILE, "w") as file:
                json.dump(bancas, file, indent=4)
            print(f"Dados salvos com sucesso em {BancaModel.DATA_FILE}")
        except IOError as e:
            print(f"Erro ao salvar dados: {e}")

    @staticmethod
    def adicionar_banca(aluno_nome, orientador_nome, titulo, data):
        """Adiciona uma nova banca."""
        bancas = BancaModel.carregar_dados()
        banca = {
            "aluno_nome": aluno_nome,
            "orientador_nome": orientador_nome,
            "titulo": titulo,
            "data": data,
            "avaliadores": [],  # Inicialmente sem avaliadores
            "nota": None         # Nota pode ser adicionada depois
        }
        bancas.append(banca)
        BancaModel.salvar_dados(bancas)
        print("Banca adicionada com sucesso!")

    @staticmethod
    def editar_banca(index, aluno_nome, orientador_nome, titulo, data):
        """Edita uma banca existente."""
        bancas = BancaModel.carregar_dados()
        if 0 <= index < len(bancas):
            bancas[index].update({
                "aluno_nome": aluno_nome,
                "orientador_nome": orientador_nome,
                "titulo": titulo,
                "data": data
            })
            BancaModel.salvar_dados(bancas)
            print(f"Banca de índice {index} editada com sucesso!")
        else:
            print("Índice inválido! Não foi possível editar a banca.")

    @staticmethod
    def remover_banca(index):
        """Remove uma banca pelo índice."""
        bancas = BancaModel.carregar_dados()
        if 0 <= index < len(bancas):
            bancas.pop(index)
            BancaModel.salvar_dados(bancas)
            print(f"Banca de índice {index} removida com sucesso!")
        else:
            print("Índice inválido! Não foi possível remover a banca.")

    @staticmethod
    def listar_bancas():
        """Retorna todas as bancas cadastradas."""
        return BancaModel.carregar_dados()

    @staticmethod
    def atribuir_avaliadores(index, avaliadores):
        """Atribui uma lista de avaliadores a uma banca específica."""
        bancas = BancaModel.carregar_dados()
        if 0 <= index < len(bancas):
            bancas[index]["avaliadores"] = avaliadores
            BancaModel.salvar_dados(bancas)
            print(f"Avaliadores atribuídos à banca de índice {index}.")
        else:
            print("Índice inválido! Não foi possível atribuir avaliadores.")

    @staticmethod
    def registrar_nota(index, nota):
        """Registra a nota de uma banca específica."""
        bancas = BancaModel.carregar_dados()
        if 0 <= index < len(bancas):
            bancas[index]["nota"] = nota
            BancaModel.salvar_dados(bancas)
            print(f"Nota {nota} registrada para a banca de índice {index}.")
        else:
            print("Índice inválido! Não foi possível registrar a nota.")
