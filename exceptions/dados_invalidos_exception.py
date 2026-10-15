class DadosInvalidosException(Exception):
    def __init__(self, mensagem: str = "Os dados informados são inválidos."):
        super().__init__(mensagem)