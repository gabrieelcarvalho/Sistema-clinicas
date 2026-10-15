class PacienteNaoCadastradoException(Exception):
    def __init__(self, cpf: str):
        self.mensagem = f"O paciente com CPF '{cpf}' não está cadastrado no sistema!"
        super().__init__(self.mensagem)