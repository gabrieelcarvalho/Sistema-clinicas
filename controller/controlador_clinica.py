from datetime import time
from model.clinica import Clinica
from view.tela_clinica import TelaClinica


class ControladorClinica:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_clinica = TelaClinica()
        self.__clinicas = []

    @property
    def clinicas(self) -> list:
        return self.__clinicas

    def cadastra_clinica(self, clinica: Clinica) -> None:
        if isinstance(clinica, Clinica):
            if self.busca_clinica(clinica.nome) is None:
                self.__clinicas.append(clinica)
                self.__tela_clinica.mostra_mensagem("Clínica cadastrada com sucesso!")
            else:
                self.__tela_clinica.mostra_mensagem("Erro: Já existe uma clínica com este nome!")

    def exclui_clinica(self, nome: str) -> None:
        clinica = self.busca_clinica(nome)
        if clinica is not None:
            self.__clinicas.remove(clinica)
            self.__tela_clinica.mostra_mensagem("Clínica excluída com sucesso!")
        else:
            self.__tela_clinica.mostra_mensagem("Erro: Clínica não encontrada!")

    def altera_horario(self, clinica: Clinica, abertura: time, fechamento: time) -> None:
        if isinstance(clinica, Clinica):
            clinica.horario_abertura = abertura
            clinica.horario_fechamento = fechamento
            self.__tela_clinica.mostra_mensagem("Horário alterado com sucesso!")

    def clinicas_abertas(self, hora: time) -> list:
        abertas = []
        for clinica in self.__clinicas:
            if hasattr(clinica, 'horario_abertura') and hasattr(clinica, 'horario_fechamento'):
                if clinica.horario_abertura <= hora <= clinica.horario_fechamento:
                    abertas.append(clinica)
        return abertas

    def busca_clinica(self, nome: str) -> Clinica | None:
        for clinica in self.__clinicas:
            if clinica.nome == nome:
                return clinica
        return None

    def abre_tela(self) -> None:
        def cadastra():
            dados = self.__tela_clinica.pega_dados_clinica()
            if dados and dados["nome"]:
                nova_clinica = Clinica(
                    nome=dados["nome"],
                    horario_abertura=dados["abertura"],
                    horario_fechamento=dados["fechamento"],
                )
                self.cadastra_clinica(nova_clinica)

        def excluir():
            nome = self.__tela_clinica.seleciona_clinica()
            if nome:
                self.exclui_clinica(nome)

        def alterar_horario():
            nome = self.__tela_clinica.seleciona_clinica()
            clinica = self.busca_clinica(nome)
            if clinica is not None:
                dados = self.__tela_clinica.pega_dados_clinica()
                self.altera_horario(clinica, dados["abertura"], dados["fechamento"])
            else:
                self.__tela_clinica.mostra_mensagem("Erro: Clínica não encontrada!")

        def listar_abertas():
            hora_str = input("Digite o horário para consulta (HH:MM): ").strip()
            try:
                h, m = map(int, hora_str.split(":"))
                hora = time(h, m)
            except ValueError:
                self.__tela_clinica.mostra_mensagem("Erro: Horário inválido!")
                return

            abertas = self.clinicas_abertas(hora)
            if abertas:
                for c in abertas:
                    self.__tela_clinica.mostra_clinica({
                        "nome": c.nome,
                        "abertura": c.horario_abertura,
                        "fechamento": c.horario_fechamento,
                    })
            else:
                self.__tela_clinica.mostra_mensagem("Nenhuma clínica aberta neste horário.")

        lista_opcoes = {
            1: cadastra,
            2: excluir,
            3: alterar_horario,
            4: listar_abertas,
            0: self.retorna,
        }

        while True:
            opcao_escolhida = self.__tela_clinica.tela_opcoes()
            funcao_escolhida = lista_opcoes.get(opcao_escolhida)

            if funcao_escolhida:
                funcao_escolhida()
            else:
                self.__tela_clinica.mostra_mensagem("Opção inválida! Escolha um número do menu.")

            if opcao_escolhida == 0:
                break

    def retorna(self) -> None:
        pass