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

    def mostra_dados(self) -> str:
        data_formatada = self.data_nascimento.strftime("%d/%m/%Y")
        return f"{super().mostra_dados()}, Data de Nascimento: {data_formatada}"

    def maior_de_idade(self) -> bool:
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return idade >= 18
