class AcompanhanteMenorDeIdadeException(Exception):
    def __init__(self):
        super().__init__(
            "O acompanhante deve ter pelo menos 18 anos "
            "na data do atendimento!"
        )