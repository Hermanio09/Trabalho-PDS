from models.banca_model import BancaModel
from models.professor_model import ProfessorModel


class BancaController:
    def __init__(self):
        """Inicializa os modelos de Banca e Professor."""
        self.banca_model = BancaModel()
        self.professor_model = ProfessorModel()

    # Métodos relacionados às bancas
    def adicionar_banca(self, aluno_nome, orientador_nome, titulo, data):
        """Adiciona uma nova banca ao sistema."""
        self.banca_model.adicionar_banca(aluno_nome, orientador_nome, titulo, data)

    def obter_bancas(self):
        """Retorna todas as bancas cadastradas."""
        return self.banca_model.listar_bancas()

    def editar_banca(self, index, aluno_nome, orientador_nome, titulo, data):
        """Edita os detalhes de uma banca."""
        bancas = self.obter_bancas()
        if 0 <= index < len(bancas):
            self.banca_model.editar_banca(index, aluno_nome, orientador_nome, titulo, data)
        else:
            raise IndexError("Índice de banca inválido.")

    def remover_banca(self, index):
        """Remove uma banca pelo índice."""
        bancas = self.obter_bancas()
        if 0 <= index < len(bancas):
            self.banca_model.remover_banca(index)
        else:
            raise IndexError("Índice de banca inválido.")

    def buscar_bancas(self, termo):
        """
        Busca bancas pelo termo informado.
        O termo é comparado ao nome do aluno, orientador e título da banca.
        """
        bancas = self.obter_bancas()
        return [
            banca
            for banca in bancas
            if termo.lower() in banca["aluno_nome"].lower()
            or termo.lower() in banca["orientador_nome"].lower()
            or termo.lower() in banca["titulo"].lower()
        ]

    def ordenar_bancas_por_nome(self):
        """Ordena as bancas pelo nome do aluno e retorna a lista ordenada."""
        bancas = self.obter_bancas()
        return sorted(bancas, key=lambda x: x["aluno_nome"])

    def atribuir_banca(self, index, professores_siape):
        """
        Atribui avaliadores a uma banca específica.
        'professores_siape' é uma lista de SIAPEs dos professores avaliadores.
        """
        bancas = self.obter_bancas()
        if 0 <= index < len(bancas):
            bancas[index]["avaliadores"] = professores_siape
            self.banca_model.salvar_dados(bancas)
        else:
            raise IndexError("Índice de banca inválido.")

    def registrar_nota(self, index, nota):
        """
        Registra a nota final de uma banca específica.
        """
        bancas = self.obter_bancas()
        if 0 <= index < len(bancas):
            bancas[index]["nota"] = nota
            self.banca_model.salvar_dados(bancas)
        else:
            raise IndexError("Índice de banca inválido.")

    # Métodos relacionados aos professores
    def cadastrar_professor(self, siape, nome, senha):
        """Cadastra um professor no sistema."""
        self.professor_model.cadastrar_professor(siape, nome, senha)

    def autenticar_professor(self, siape, senha):
        """Autentica um professor pelo SIAPE e senha."""
        return self.professor_model.autenticar_professor(siape, senha)
