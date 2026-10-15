class PagamentoExcedenteException(Exception):
    def __init__(self, mensagem: str = "O pagamento excede o valor restante do atendimento."):
        super().__init__(mensagem)