from model.profissional import Profissional

class Procedimento:
    def __init__(self, descricao: str, custo: float, profissional: Profissional):
        self.__descricao = descricao
        self.__custo = custo
        self.__profissional = profissional

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @property
    def custo(self) -> float:
        return self.__custo

    @custo.setter
    def custo(self, custo: float):
        self.__custo = custo

    @property
    def profissional(self) -> Profissional:
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional: Profissional):
        self.__profissional = profissional

    def mostra_dados(self) -> str:
        return f"Descrição: {self.descricao}, Custo: R$ {self.custo:.2f}, Profissional: {self.profissional.nome}"