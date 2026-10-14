class TipoAtendimento:
    def __init__(self, codigo: int, nome: str):
        self.__codigo = codigo
        self.__nome = nome

    @property
    def codigo(self) -> int:
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo: int):
        self.__codigo = codigo

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    def mostra_dados(self) -> str:
        return f"Código: {self.codigo}, Nome: {self.nome}"