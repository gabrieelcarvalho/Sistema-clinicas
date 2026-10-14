
from datetime import date
from model.pessoa import Pessoa


class Paciente(Pessoa):
    def __init__(self, cpf: str, nome: str, celular: str, data_nascimento: date):
        super().__init__(cpf, nome, celular)
        self.__data_nascimento = data_nascimento

    @property
    def data_nascimento(self) -> date:
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: date):
        self.__data_nascimento = data_nascimento

    def maior_de_idade(self, data_referencia: date = None) -> bool:
        if data_referencia is None:
            data_referencia = date.today()

        idade = data_referencia.year - self.data_nascimento.year

        if (data_referencia.month, data_referencia.day) < (
            self.data_nascimento.month, self.data_nascimento.day
        ):
            idade -= 1

        return idade >= 18

    def mostra_dados(self) -> str:
        return (
            f"{super().mostra_dados()}, "
            f"Data de Nascimento: {self.data_nascimento:%d/%m/%Y}"
        )
