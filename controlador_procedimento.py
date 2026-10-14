from model.procedimento import Procedimento
from view.tela_procedimento import TelaProcedimento
from controller.controlador_sistema import ControladorSistema


class ControladorProcedimento:
    def __init__(self, controlador_sistema: ControladorSistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_procedimento = TelaProcedimento()
        self.__procedimentos = []

    @property
    def procedimentos(self) -> list:
        return self.__procedimentos

    def cadastra_procedimento(self, proc: Procedimento) -> None:
        if isinstance(proc, Procedimento):
            if self.busca_procedimento(proc.descricao) is None:
                self.__procedimentos.append(proc)
                self.__tela_procedimento.mostra_mensagem("Procedimento cadastrado com sucesso!")
            else:
                self.__tela_procedimento.mostra_mensagem("Erro: Já existe um procedimento com esta descrição!")

    def exclui_procedimento(self, descricao: str) -> None:
        procedimento = self.busca_procedimento(descricao)
        if procedimento is not None:
            self.__procedimentos.remove(procedimento)
            self.__tela_procedimento.mostra_mensagem("Procedimento excluído com sucesso!")
        else:
            self.__tela_procedimento.mostra_mensagem("Erro: Procedimento não encontrado!")

    def busca_procedimento(self, descricao: str) -> Procedimento | None:
        for procedimento in self.__procedimentos:
            if procedimento.descricao == descricao:
                return procedimento
        return None

    def abre_tela(self) -> None:
        def cadastra():
            dados = self.__tela_procedimento.pega_dados_procedimento()
            if dados:
                novo_procedimento = Procedimento(
                    descricao=dados["descricao"],
                    custo=dados["custo"]
                )
                self.cadastra_procedimento(novo_procedimento)

        def excluir():
            descricao = self.__tela_procedimento.seleciona_procedimento()
            if descricao:
                self.exclui_procedimento(descricao)

        lista_opcoes = {
            1: cadastra,
            2: excluir,
            0: self.retorna,
        }

        while True:
            opcao_escolhida = self.__tela_procedimento.tela_opcoes()
            funcao_escolhida = lista_opcoes.get(opcao_escolhida)

            if funcao_escolhida:
                funcao_escolhida()
            else:
                self.__tela_procedimento.mostra_mensagem("Opção inválida! Escolha um número do menu.")

            if opcao_escolhida == 0:
                break

    def retorna(self) -> None:
        pass