
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

    def busca_paciente(self, cpf: str):
        return next(
            (p for p in self.__pacientes if p.cpf == cpf),
            None
        )

    def cadastra_paciente(self, paciente: Paciente) -> None:
        if (
            not isinstance(paciente, Paciente)
            or not paciente.nome.strip()
            or not paciente.cpf.strip()
        ):
            self.__tela_paciente.mostra_mensagem(
                "Dados do paciente inválidos!"
            )
        elif self.busca_paciente(paciente.cpf) is not None:
            self.__tela_paciente.mostra_mensagem(
                "Já existe paciente com esse CPF!"
            )
        else:
            self.__pacientes.append(paciente)
            self.__tela_paciente.mostra_mensagem(
                "Paciente cadastrado com sucesso!"
            )

    def exclui_paciente(self, cpf: str) -> None:
        paciente = self.busca_paciente(cpf)

        if paciente is None:
            self.__tela_paciente.mostra_mensagem(
                "Paciente não encontrado!"
            )
        elif any(
            a.paciente is paciente
            for a in self.__controlador_sistema
            .controlador_atendimento.atendimentos
        ):
            self.__tela_paciente.mostra_mensagem(
                "Paciente possui atendimentos. "
                "Cancele-os antes da exclusão."
            )
        else:
            self.__pacientes.remove(paciente)
            self.__tela_paciente.mostra_mensagem(
                "Paciente excluído com sucesso!"
            )

    def altera_nome(
        self, cpf: str, novo_nome: str
    ) -> None:
        self.__altera_texto(
            cpf, "nome", novo_nome
        )

    def altera_cpf(
        self, cpf_atual: str, novo_cpf: str
    ) -> None:
        paciente = self.busca_paciente(cpf_atual)

        if paciente is None or not novo_cpf.strip():
            self.__tela_paciente.mostra_mensagem(
                "Paciente não encontrado ou CPF inválido!"
            )
        elif self.busca_paciente(novo_cpf) not in (
            None, paciente
        ):
            self.__tela_paciente.mostra_mensagem(
                "Novo CPF já cadastrado!"
            )
        else:
            paciente.cpf = novo_cpf
            self.__tela_paciente.mostra_mensagem(
                "CPF alterado com sucesso!"
            )

    def altera_celular(
        self, cpf: str, novo_celular: str
    ) -> None:
        self.__altera_texto(
            cpf, "celular", novo_celular
        )

    def __altera_texto(
        self, cpf: str, campo: str, valor: str
    ) -> None:
        paciente = self.busca_paciente(cpf)

        if paciente is None or not valor.strip():
            self.__tela_paciente.mostra_mensagem(
                "Paciente não encontrado ou dado vazio!"
            )
            return

        setattr(paciente, campo, valor)

        self.__tela_paciente.mostra_mensagem(
            "Dado alterado com sucesso!"
        )

    def altera_data_nascimento(
        self, cpf, nova_data
    ) -> None:
        paciente = self.busca_paciente(cpf)

        if paciente is None:
            self.__tela_paciente.mostra_mensagem(
                "Paciente não encontrado!"
            )
            return

        atendimentos = (
            self.__controlador_sistema
            .controlador_atendimento.atendimentos
        )

        if any(
            a.paciente is paciente
            and not Paciente(
                paciente.cpf,
                paciente.nome,
                paciente.celular,
                nova_data
            ).maior_de_idade(a.data)
            and a.acompanhante is None
            for a in atendimentos
        ):
            self.__tela_paciente.mostra_mensagem(
                "Nova data tornaria um atendimento "
                "de menor inválido!"
            )
            return

        paciente.data_nascimento = nova_data

        self.__tela_paciente.mostra_mensagem(
            "Data de nascimento alterada!"
        )

    def retorna(self) -> None:
        pass

    def __incluir(self):
        dados = self.__tela_paciente.pega_dados_paciente()
        self.cadastra_paciente(Paciente(**dados))

    def __listar(self):
        if not self.__pacientes:
            self.__tela_paciente.mostra_mensagem(
                "Nenhum paciente cadastrado."
            )

        for p in self.__pacientes:
            self.__tela_paciente.mostra_paciente({
                "nome": p.nome,
                "cpf": p.cpf,
                "celular": p.celular,
                "data_nascimento": p.data_nascimento
            })

    def __excluir(self):
        cpf = self.__tela_paciente.seleciona_paciente()
        self.exclui_paciente(cpf)

    def __editar(self, campo: str):
        cpf = self.__tela_paciente.seleciona_paciente()
        valor = self.__tela_paciente.pega_novo_dado(
            campo
        )

        {
            "nome": self.altera_nome,
            "cpf": self.altera_cpf,
            "celular": self.altera_celular
        }[campo](cpf, valor)

    def __editar_nascimento(self):
        cpf = self.__tela_paciente.seleciona_paciente()
        nova_data = (
            self.__tela_paciente
            .pega_nova_data_nascimento()
        )

        self.altera_data_nascimento(
            cpf, nova_data
        )

    def abre_tela(self):
        opcoes = {
            1: self.__incluir,
            2: self.__excluir,
            3: lambda: self.__editar("nome"),
            4: lambda: self.__editar("cpf"),
            5: self.__listar,
            6: lambda: self.__editar("celular"),
            7: self.__editar_nascimento,
            0: self.retorna
        }

        while True:
            opcao = self.__tela_paciente.tela_opcoes()

            if opcao not in opcoes:
                self.__tela_paciente.mostra_mensagem(
                    "Opção inválida!"
                )
                continue

            opcoes[opcao]()

            if opcao == 0:
                break
