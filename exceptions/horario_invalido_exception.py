class HorarioInvalidoException(Exception):
    def __init__(self, mensagem: str = "O horário final deve ser posterior ao inicial."):
        super().__init__(mensagem)