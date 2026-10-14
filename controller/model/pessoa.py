from abc import ABC, abstractmethod

class Pessoa(ABC):
    def __init__(self, cpf: str, nome: str, celular: str):
        self.__cpf = cpf
        self.__nome = nome
        self.__celular = celular

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str):
        self.__cpf = cpf

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, celular: str):
        self.__celular = celular

    @abstractmethod
    def mostra_dados(self) -> str:
        return f"Nome: {self.nome}, CPF: {self.cpf}, Celular: {self.celular}"