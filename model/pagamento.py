
from abc import ABC, abstractmethod
from datetime import date as Date
from model.atendimento import Atendimento


class Pagamento(ABC):
    def __init__(
        self, data: Date, atendimento: Atendimento,
        valor_pagamento: float
    ):
        self.__data = data
        self.__atendimento = atendimento
        self.__valor_pagamento = valor_pagamento

    @property
    def data(self) -> Date:
        return self.__data

    @data.setter
    def data(self, valor: Date):
        self.__data = valor

    @property
    def atendimento(self) -> Atendimento:
        return self.__atendimento

    @atendimento.setter
    def atendimento(self, valor: Atendimento):
        self.__atendimento = valor

    @property
    def valor_pagamento(self) -> float:
        return self.__valor_pagamento

    @valor_pagamento.setter
    def valor_pagamento(self, valor: float):
        self.__valor_pagamento = valor

    def paciente(self):
        return self.atendimento.paciente

    @abstractmethod
    def mostra_dados(self) -> str:
        return (
            f"Data: {self.data:%d/%m/%Y}, "
            f"Atendimento Nº: {self.atendimento.numero_atendimento}, "
            f"Valor Pago: R$ {self.valor_pagamento:.2f}"
        )
