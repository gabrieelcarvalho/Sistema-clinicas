from model.paciente import Paciente
from view.tela_paciente import TelaPaciente


class ControladorPaciente:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_paciente = TelaPaciente()
        self.__pacientes = []

    @property
    def pacientes(self) -> list:
        return self.__pacientes

    def cadastra_paciente(self, paciente: Paciente) -> None:
        if isinstance(paciente, Paciente):
            if self.busca_paciente(paciente.cpf) is None:
                self.__pacientes.append(paciente)
                self.__tela_paciente.mostra_mensagem("Paciente cadastrado com sucesso!")
            else:
                self.__tela_paciente.mostra_mensagem("Erro: Já existe um paciente com este CPF!")

    def exclui_paciente(self, cpf: str) -> None:
        paciente = self.busca_paciente(cpf)
        if paciente is not None:
            self.__pacientes.remove(paciente)
            self.__tela_paciente.mostra_mensagem("Paciente excluído com sucesso!")
        else:
            self.__tela_paciente.mostra_mensagem("Erro: Paciente não encontrado!")

    def altera_nome(self, cpf: str, novo_nome: str) -> None:
        paciente = self.busca_paciente(cpf)
        if paciente is not None:
            paciente.nome = novo_nome
            self.__tela_paciente.mostra_mensagem("Nome alterado com sucesso!")
        else:
            self.__tela_paciente.mostra_mensagem("Erro: Paciente não encontrado!")

    def altera_cpf(self, cpf_atual: str, novo_cpf: str) -> None:
        paciente = self.busca_paciente(cpf_atual)
        if paciente is not None:
            if self.busca_paciente(novo_cpf) is None:
                paciente.cpf = novo_cpf
                self.__tela_paciente.mostra_mensagem("CPF alterado com sucesso!")
            else:
                self.__tela_paciente.mostra_mensagem("Erro: Já existe um paciente com este novo CPF!")
        else:
            self.__tela_paciente.mostra_mensagem("Erro: Paciente não encontrado!")

    def busca_paciente(self, cpf: str) -> Paciente | None:
        for paciente in self.__pacientes:
            if paciente.cpf == cpf:
                return paciente
        return None

    def abre_tela(self) -> None:
        def cadastra():
            dados = self.__tela_paciente.pega_dados_paciente()
            if dados:
                novo_paciente = Paciente(
                    cpf=dados["cpf"],
                    nome=dados["nome"],
                    celular=dados["celular"],
                    data_nascimento=dados["data_nascimento"],
                )
                self.cadastra_paciente(novo_paciente)

        def excluir():
            cpf = self.__tela_paciente.seleciona_paciente()
            if cpf:
                self.exclui_paciente(cpf)

        def alterar_nome():
            cpf = self.__tela_paciente.seleciona_paciente()
            if cpf:
                novo_nome = input("Digite o novo nome: ").strip()
                if novo_nome:
                    self.altera_nome(cpf, novo_nome)

        def alterar_cpf():
            cpf_atual = self.__tela_paciente.seleciona_paciente()
            if cpf_atual:
                novo_cpf = input("Digite o novo CPF: ").strip()
                if novo_cpf:
                    self.altera_cpf(cpf_atual, novo_cpf)

        lista_opcoes = {
            1: cadastra,
            2: excluir,
            3: alterar_nome,
            4: alterar_cpf,
            0: self.retorna,
        }

        while True:
            opcao_escolhida = self.__tela_paciente.tela_opcoes()
            funcao_escolhida = lista_opcoes.get(opcao_escolhida)

            if funcao_escolhida:
                funcao_escolhida()
            else:
                self.__tela_paciente.mostra_mensagem("Opção inválida! Escolha um número do menu.")

            if opcao_escolhida == 0:
                break

    def retorna(self) -> None:
        pass