from datetime import date
from model.pessoa import Pessoa

class Acompanhante(Pessoa):
    def __init__(self, cpf: str, nome: str, celular: str, data_nascimento: date, relacao_paciente: str):
        super().__init__(cpf, nome, celular)
        self.__data_nascimento = data_nascimento
        self.__relacao_paciente = relacao_paciente

    @property
    def data_nascimento(self) -> date: 
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: date):
        self.__data_nascimento = data_nascimento

    @property
    def relacao_paciente(self) -> str:
        return self.__relacao_paciente

    @relacao_paciente.setter
    def relacao_paciente(self, relacao_paciente: str):
        self.__relacao_paciente = relacao_paciente

    def mostra_dados(self) -> str:
        data_formatada = self.data_nascimento.strftime("%d/%m/%Y")
        return f"{super().mostra_dados()}, Data de Nascimento: {data_formatada}, Relação com o Paciente: {self.relacao_paciente}"
    