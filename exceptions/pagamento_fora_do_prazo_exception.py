class PagamentoForaDoPrazoException(Exception):
    def __init__(self, mensagem: str = "O pagamento deve ocorrer até a data do atendimento."):
        super().__init__(mensagem)