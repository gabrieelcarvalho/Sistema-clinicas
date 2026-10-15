from datetime import date as Date
from model.pagamento import Pagamento


class PagamentoCartao(Pagamento):
    def __init__(
        self,
        data: Date,
        atendimento,
        valor_pagamento: float,
        bandeira: str,
        numero: str
    ):
        super().__init__(data, atendimento, valor_pagamento)
        self.__bandeira = bandeira
        self.__numero = numero

    @property
    def bandeira(self) -> str:
        return self.__bandeira

    @bandeira.setter
    def bandeira(self, bandeira: str) -> None:
        self.__bandeira = bandeira

    @property
    def numero(self) -> str:
        return self.__numero

    @numero.setter
    def numero(self, numero: str) -> None:
        self.__numero = numero

    def mostra_dados(self) -> str:
        return (
            f"Pagamento Cartão - Valor: R$ {self.valor_pagamento:.2f} | "
            f"Data: {self.data.strftime('%d/%m/%Y')} | "
            f"Bandeira: {self.__bandeira} | Número: {self.__numero}"
        )