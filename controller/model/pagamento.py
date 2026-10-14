from abc import ABC, abstractmethod
from datetime import date as Date
from model.atendimento import Atendimento


class Pagamento(ABC):
    def __init__(self, data: Date, atendimento: Atendimento, valor_pagamento: float):
        self.__data = data
        self.__atendimento = atendimento
        self.__valor_pagamento = valor_pagamento

    @property
    def data(self) -> Date:
        return self.__data

    @data.setter
    def data(self, data: Date):
        self.__data = data

    @property
    def atendimento(self) -> Atendimento:
        return self.__atendimento

    @atendimento.setter
    def atendimento(self, atendimento: Atendimento):
        self.__atendimento = atendimento

    @property
    def valor_pagamento(self) -> float:
        return self.__valor_pagamento

    @valor_pagamento.setter
    def valor_pagamento(self, valor_pagamento: float):
        self.__valor_pagamento = valor_pagamento

    @abstractmethod
    def mostra_dados(self) -> str:
        data_f = self.data.strftime("%d/%m/%Y")
        return (
            f"Data: {data_f}, "
            f"Atendimento Nº: {self.atendimento.numero_atendimento}, "
            f"Valor Pago: R$ {self.valor_pagamento:.2f}"
        )