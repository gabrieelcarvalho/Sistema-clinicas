class ValorPagamentoInvalidoException(Exception):
    def __init__(self, mensagem: str = "O valor do pagamento deve ser maior que zero."):
        super().__init__(mensagem)