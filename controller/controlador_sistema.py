import sys
from view.tela_sistema import TelaSistema
from controller.controlador_paciente import ControladorPaciente
from controller.controlador_profissional import ControladorProfissional
from controller.controlador_clinica import ControladorClinica
from controller.controlador_atendimento import ControladorAtendimento
from controller.controlador_tipo_atendimento import ControladorTipoAtendimento
from controller.controlador_procedimento import ControladorProcedimento
from controller.controlador_relatorio import ControladorRelatorio


class ControladorSistema:
    def __init__(self):
        self.__tela_sistema = TelaSistema()

        self.__controlador_paciente = ControladorPaciente(self)
        self.__controlador_profissional = ControladorProfissional(self)
        self.__controlador_clinica = ControladorClinica(self)
        self.__controlador_atendimento = ControladorAtendimento(self)
        self.__controlador_tipo_atendimento = ControladorTipoAtendimento(self)
        self.__controlador_procedimento = ControladorProcedimento(self)
        self.__controlador_relatorio = ControladorRelatorio(self)

    @property
    def controlador_paciente(self) -> ControladorPaciente:
        return self.__controlador_paciente

    @property
    def controlador_profissional(self) -> ControladorProfissional:
        return self.__controlador_profissional

    @property
    def controlador_clinica(self) -> ControladorClinica:
        return self.__controlador_clinica

    @property
    def controlador_atendimento(self) -> ControladorAtendimento:
        return self.__controlador_atendimento

    @property
    def controlador_tipo_atendimento(self) -> ControladorTipoAtendimento:
        return self.__controlador_tipo_atendimento

    @property
    def controlador_procedimento(self) -> ControladorProcedimento:
        return self.__controlador_procedimento

    @property
    def controlador_relatorio(self) -> ControladorRelatorio:
        return self.__controlador_relatorio

    def abre_tela_clinica(self) -> None:
        self.__controlador_clinica.abre_tela()

    def abre_tela_paciente(self) -> None:
        self.__controlador_paciente.abre_tela()

    def abre_tela_profissional(self) -> None:
        self.__controlador_profissional.abre_tela()

    def abre_tela_tipo_atendimento(self) -> None:
        self.__controlador_tipo_atendimento.abre_tela()

    def abre_tela_procedimento(self) -> None:
        self.__controlador_procedimento.abre_tela()

    def abre_tela_atendimento(self) -> None:
        self.__controlador_atendimento.abre_tela()

    def abre_tela_relatorio(self) -> None:
        self.__controlador_relatorio.abre_tela()

    def encerra_sistema(self) -> None:
        self.__tela_sistema.mostra_mensagem("Encerrando o sistema... Até logo!")
        sys.exit(0)

    def inicializa_sistema(self) -> None:
        lista_opcoes = {
            1: self.abre_tela_clinica,
            2: self.abre_tela_paciente,
            3: self.abre_tela_profissional,
            4: self.abre_tela_tipo_atendimento,
            5: self.abre_tela_procedimento,
            6: self.abre_tela_atendimento,
            7: self.abre_tela_relatorio,
            0: self.encerra_sistema
        }

        while True:
            opcao_escolhida = self.__tela_sistema.tela_opcoes()
            funcao_escolhida = lista_opcoes.get(opcao_escolhida)

            if funcao_escolhida:
                funcao_escolhida()
            else:
                self.__tela_sistema.mostra_mensagem("Opção inválida! Escolha um número do menu.")