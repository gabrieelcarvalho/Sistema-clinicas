
from datetime import time as Time


class Clinica:
    def __init__(self, nome: str, cidade: str, descricao: str,
                 horario_abertura: Time, horario_fechamento: Time):
        self.__nome = nome
        self.__cidade = cidade
        self.__descricao = descricao
        self.__horario_abertura = horario_abertura
        self.__horario_fechamento = horario_fechamento
        self.__profissionais = []
        self.__pacientes = []
        self.__atendimentos = []

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def cidade(self) -> str:
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade: str):
        self.__cidade = cidade

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @property
    def horario_abertura(self) -> Time:
        return self.__horario_abertura

    @horario_abertura.setter
    def horario_abertura(self, horario_abertura: Time):
        self.__horario_abertura = horario_abertura

    @property
    def horario_fechamento(self) -> Time:
        return self.__horario_fechamento

    @horario_fechamento.setter
    def horario_fechamento(self, horario_fechamento: Time):
        self.__horario_fechamento = horario_fechamento

    @property
    def profissionais(self) -> list:
        return self.__profissionais

    @property
    def pacientes(self) -> list:
        return self.__pacientes

    @property
    def atendimentos(self) -> list:
        return self.__atendimentos

    def esta_aberta_clinica(
        self, horario_inicio: Time, horario_fim: Time = None
    ) -> bool:
        if self.horario_abertura >= self.horario_fechamento:
            return False

        if horario_fim is None:
            return (
                self.horario_abertura <= horario_inicio
                <= self.horario_fechamento
            )

        return (
            self.horario_abertura <= horario_inicio
            < horario_fim <= self.horario_fechamento
        )

    def inclui_paciente(self, paciente):
        if paciente not in self.__pacientes:
            self.__pacientes.append(paciente)

    def exclui_paciente(self, paciente):
        if paciente in self.__pacientes:
            self.__pacientes.remove(paciente)

    def inclui_profissional(self, profissional):
        if profissional not in self.__profissionais:
            self.__profissionais.append(profissional)

    def exclui_profissional(self, profissional):
        if profissional in self.__profissionais:
            self.__profissionais.remove(profissional)

    def registra_atendimento(self, atendimento):
        if atendimento not in self.__atendimentos:
            self.__atendimentos.append(atendimento)

    def cancela_atendimento(self, atendimento):
        if atendimento in self.__atendimentos:
            self.__atendimentos.remove(atendimento)

    def mostra_dados(self) -> str:
        return (
            f"Nome: {self.nome}, Cidade: {self.cidade}, "
            f"Descrição: {self.descricao}, "
            f"Horário de Funcionamento: "
            f"{self.horario_abertura:%H:%M} às "
            f"{self.horario_fechamento:%H:%M}"
        )
