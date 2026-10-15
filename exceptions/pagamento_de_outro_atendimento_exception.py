class PagamentoDeOutroAtendimentoException(Exception):
    def __init__(self, mensagem: str = "O pagamento não pertence a este atendimento."):
        super().__init__(mensagem)