class AtendimentoForaDoHorarioException(Exception):
    def __init__(self, mensagem: str = "O atendimento deve ocorrer dentro do horário da clínica."):
        super().__init__(mensagem)