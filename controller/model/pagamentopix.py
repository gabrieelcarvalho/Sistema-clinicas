from datetime import date as Date
from model.pagamento import Pagamento
from model.atendimento import Atendimento


class PagamentoPix(Pagamento):
    def __init__(
        self, data: Date, atendimento: Atendimento, valor_pagamento: float, cpf: str
    ):
        super().__init__(data, atendimento, valor_pagamento)
        self.__cpf = cpf

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str):
        self.__cpf = cpf

    def mostra_dados(self) -> str:
        return f"{super().mostra_dados()}, Forma: PIX (CPF/Chave: {self.cpf})"