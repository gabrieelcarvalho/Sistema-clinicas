class ConflitoDeHorarioException(Exception):
    def __init__(self, mensagem: str = "O profissional já possui atendimento nesse horário."):
        super().__init__(mensagem)