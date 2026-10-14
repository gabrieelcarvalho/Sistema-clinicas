
from model.profissional import Profissional
from view.tela_profissional import TelaProfissional


class ControladorProfissional:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_profissional = TelaProfissional()
        self.__profissionais = []

    @property
    def profissionais(self) -> list:
        return self.__profissionais

    def busca_profissional(self, cpf: str):
        return next(
            (p for p in self.__profissionais if p.cpf == cpf),
            None
        )

    def __busca_registro(self, registro: str):
        return next(
            (
                p for p in self.__profissionais
                if p.registro_profissional == registro
            ),
            None
        )

    def cadastra_profissional(
        self, profissional: Profissional
    ) -> None:
        if (
            not isinstance(profissional, Profissional)
            or not profissional.cpf
            or not profissional.registro_profissional
            or not profissional.nome
        ):
            self.__tela_profissional.mostra_mensagem(
                "Dados inválidos!"
            )

        elif (
            self.busca_profissional(profissional.cpf)
            or self.__busca_registro(
                profissional.registro_profissional
            )
        ):
            self.__tela_profissional.mostra_mensagem(
                "CPF ou registro profissional já cadastrado!"
            )

        else:
            self.__profissionais.append(profissional)
            self.__tela_profissional.mostra_mensagem(
                "Profissional cadastrado com sucesso!"
            )

    def exclui_profissional(self, cpf: str) -> None:
        profissional = self.busca_profissional(cpf)

        if profissional is None:
            self.__tela_profissional.mostra_mensagem(
                "Profissional não encontrado!"
            )

        elif any(
            a.profissional is profissional
            for a in self.__controlador_sistema
            .controlador_atendimento.atendimentos
        ):
            self.__tela_profissional.mostra_mensagem(
                "Profissional possui atendimentos vinculados!"
            )

        elif any(
            p.profissional is profissional
            for p in self.__controlador_sistema
            .controlador_procedimento.procedimentos
        ):
            self.__tela_profissional.mostra_mensagem(
                "Profissional possui procedimentos vinculados!"
            )

        else:
            self.__profissionais.remove(profissional)
            self.__tela_profissional.mostra_mensagem(
                "Profissional excluído!"
            )

    def altera_especialidade(
        self, registro: str, nova_especialidade: str
    ) -> None:
        profissional = self.__busca_registro(registro)

        self.__altera_texto(
            profissional, "especialidade",
            nova_especialidade
        )

    def altera_registro(
        self, registro_atual: str, novo_registro: str
    ) -> None:
        profissional = self.__busca_registro(
            registro_atual
        )

        if profissional is None or not novo_registro:
            self.__tela_profissional.mostra_mensagem(
                "Registro inválido ou profissional não encontrado!"
            )

        elif self.__busca_registro(
            novo_registro
        ) not in (None, profissional):
            self.__tela_profissional.mostra_mensagem(
                "Registro já utilizado!"
            )

        else:
            profissional.registro_profissional = novo_registro
            self.__tela_profissional.mostra_mensagem(
                "Registro alterado!"
            )

    def altera_nome(
        self, cpf: str, novo_nome: str
    ) -> None:
        self.__altera_texto(
            self.busca_profissional(cpf),
            "nome", novo_nome
        )

    def altera_cpf(
        self, cpf_atual: str, novo_cpf: str
    ) -> None:
        profissional = self.busca_profissional(cpf_atual)

        if profissional is None or not novo_cpf:
            self.__tela_profissional.mostra_mensagem(
                "CPF inválido ou profissional não encontrado!"
            )

        elif self.busca_profissional(
            novo_cpf
        ) not in (None, profissional):
            self.__tela_profissional.mostra_mensagem(
                "CPF já utilizado!"
            )

        else:
            profissional.cpf = novo_cpf
            self.__tela_profissional.mostra_mensagem(
                "CPF alterado!"
            )

    def altera_celular(
        self, cpf: str, novo_celular: str
    ) -> None:
        self.__altera_texto(
            self.busca_profissional(cpf),
            "celular", novo_celular
        )

    def __altera_texto(
        self, profissional, campo: str, valor: str
    ):
        if profissional is None or not valor.strip():
            self.__tela_profissional.mostra_mensagem(
                "Profissional não encontrado ou valor vazio!"
            )
            return

        setattr(profissional, campo, valor)

        self.__tela_profissional.mostra_mensagem(
            "Dado alterado com sucesso!"
        )

    def __incluir(self):
        dados = (
            self.__tela_profissional
            .pega_dados_profissional()
        )

        self.cadastra_profissional(
            Profissional(**dados)
        )

    def __excluir(self):
        cpf = (
            self.__tela_profissional
            .seleciona_profissional()
        )

        self.exclui_profissional(cpf)

    def __listar(self):
        if not self.__profissionais:
            self.__tela_profissional.mostra_mensagem(
                "Nenhum profissional cadastrado."
            )

        for p in self.__profissionais:
            self.__tela_profissional.mostra_profissional({
                "nome": p.nome,
                "cpf": p.cpf,
                "celular": p.celular,
                "especialidade": p.especialidade,
                "registro_profissional": p.registro_profissional
            })

    def __editar(self, campo: str):
        tipo = (
            "registro profissional"
            if campo in ("especialidade", "registro")
            else "CPF"
        )

        identificador = (
            self.__tela_profissional
            .seleciona_profissional(tipo)
        )

        valor = (
            self.__tela_profissional
            .pega_novo_dado(campo)
        )

        {
            "especialidade": self.altera_especialidade,
            "registro": self.altera_registro,
            "nome": self.altera_nome,
            "cpf": self.altera_cpf,
            "celular": self.altera_celular
        }[campo](identificador, valor)

    def retorna(self):
        pass

    def abre_tela(self):
        opcoes = {
            1: self.__incluir,
            2: self.__excluir,
            3: lambda: self.__editar("especialidade"),
            4: lambda: self.__editar("registro"),
            5: lambda: self.__editar("nome"),
            6: lambda: self.__editar("cpf"),
            7: self.__listar,
            8: lambda: self.__editar("celular"),
            0: self.retorna
        }

        while True:
            opcao = (
                self.__tela_profissional
                .tela_opcoes()
            )

            if opcao not in opcoes:
                self.__tela_profissional.mostra_mensagem(
                    "Opção inválida!"
                )
                continue

            opcoes[opcao]()

            if opcao == 0:
                break
