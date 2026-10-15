class ProfissionalNaoCadastradoException(Exception):
    def __init__(self, cpf: str):
        self.mensagem = f"O profissional com CPF '{cpf}' não está cadastrado no sistema!"
        super().__init__(self.mensagem)