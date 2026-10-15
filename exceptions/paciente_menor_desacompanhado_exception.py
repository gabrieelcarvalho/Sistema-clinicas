class PacienteMenorDesacompanhadoException(Exception):
    def __init__(self, mensagem: str = "Paciente menor de 18 anos precisa de acompanhante."):
        super().__init__(mensagem)