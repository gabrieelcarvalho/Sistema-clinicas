class ProfissionalOcupadoException(Exception):
    def __init__(self, cpf: str = None):
        if cpf:
            super().__init__(f"O profissional com CPF '{cpf}' já possui um atendimento agendado nesse horário!")
        else:
            super().__init__("O profissional já possui um atendimento agendado nesse horário!")