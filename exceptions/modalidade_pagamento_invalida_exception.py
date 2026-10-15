class ModalidadePagamentoInvalidaException(Exception):
    def __init__(self, mensagem: str = "Modalidade de pagamento inválida."):
        super().__init__(mensagem)