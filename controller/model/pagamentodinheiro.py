from datetime import date as Date
from model.pagamento import Pagamento
from model.atendimento import Atendimento

class PagamentoDinheiro(Pagamento):
    def __init__(self, data: Date, atendimento: Atendimento, valor_pagamento: float):
        super().__init__(data, atendimento, valor_pagamento)

    def mostra_dados(self) -> str:
        return f"{super().mostra_dados()}, Forma: Dinheiro"