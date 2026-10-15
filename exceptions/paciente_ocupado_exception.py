class PacienteOcupadoException(Exception):
    def __init__(self, cpf: str = None):
        if cpf:
            super().__init__(f"O paciente com CPF '{cpf}' já possui um atendimento agendado nesse horário!")
        else:
            super().__init__("O paciente já possui um atendimento agendado nesse horário!")