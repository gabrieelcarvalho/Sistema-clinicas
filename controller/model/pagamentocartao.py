from datetime import date as Date
from model.pagamento import Pagamento
from model.atendimento import Atendimento


class PagamentoCartao(Pagamento):
    def __init__(
        self,
        data: Date,
        atendimento: Atendimento,
        valor_pagamento: float,
        bandeira: str,
        numero: str,
        parcelas: int,
    ):
        super().__init__(data, atendimento, valor_pagamento)
        self.__bandeira = bandeira
        self.__numero = numero
        self.__parcelas = parcelas

    @property
    def bandeira(self) -> str:
        return self.__bandeira

    @bandeira.setter
    def bandeira(self, bandeira: str):
        self.__bandeira = bandeira

    @property
    def numero(self) -> str:
        return self.__numero

    @numero.setter
    def numero(self, numero: str):
        self.__numero = numero

    @property
    def parcelas(self) -> int:
        return self.__parcelas

    @parcelas.setter
    def parcelas(self, parcelas: int):
        self.__parcelas = parcelas

    def mostra_dados(self) -> str:
        return (
            f"{super().mostra_dados()}, Forma: Cartão, Bandeira: {self.bandeira}, "
            f"Número: {self.numero}, Parcelas: {self.parcelas}"
        )