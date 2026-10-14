
from model.procedimento import Procedimento
from view.tela_procedimento import TelaProcedimento


class ControladorProcedimento:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_procedimento = TelaProcedimento()
        self.__procedimentos = []

    @property
    def procedimentos(self) -> list:
        return self.__procedimentos

    def busca_procedimento(self, descricao: str):
        return next(
            (
                p for p in self.__procedimentos
                if p.descricao == descricao
            ),
            None
        )

    def cadastra_procedimento(
        self, proc: Procedimento
    ) -> None:
        if (
            not isinstance(proc, Procedimento)
            or not proc.descricao.strip()
            or not 0 <= proc.custo < float("inf")
        ):
            self.__tela_procedimento.mostra_mensagem(
                "Procedimento inválido!"
            )

        elif self.busca_procedimento(
            proc.descricao
        ):
            self.__tela_procedimento.mostra_mensagem(
                "Descrição já cadastrada!"
            )

        else:
            self.__procedimentos.append(proc)
            self.__tela_procedimento.mostra_mensagem(
                "Procedimento cadastrado!"
            )

    def exclui_procedimento(
        self, descricao: str
    ) -> None:
        proc = self.busca_procedimento(descricao)

        if proc is None:
            self.__tela_procedimento.mostra_mensagem(
                "Procedimento não encontrado!"
            )

        elif any(
            proc in atendimento.procedimentos
            for atendimento in self.__controlador_sistema
            .controlador_atendimento.atendimentos
        ):
            self.__tela_procedimento.mostra_mensagem(
                "Procedimento utilizado em atendimentos. "
                "Remova os vínculos antes!"
            )

        else:
            self.__procedimentos.remove(proc)
            self.__tela_procedimento.mostra_mensagem(
                "Procedimento excluído!"
            )

    def altera_descricao(
        self, descricao_atual: str,
        nova_descricao: str
    ):
        proc = self.busca_procedimento(
            descricao_atual
        )

        if proc is None or not nova_descricao.strip():
            self.__tela_procedimento.mostra_mensagem(
                "Procedimento não encontrado "
                "ou descrição inválida!"
            )

        elif self.busca_procedimento(
            nova_descricao
        ) not in (None, proc):
            self.__tela_procedimento.mostra_mensagem(
                "Descrição já utilizada!"
            )

        else:
            proc.descricao = nova_descricao
            self.__tela_procedimento.mostra_mensagem(
                "Descrição alterada!"
            )

    def altera_custo(
        self, descricao: str, novo_custo: float
    ):
        proc = self.busca_procedimento(
            descricao
        )

        if (
            proc is None
            or not 0 <= novo_custo < float("inf")
        ):
            self.__tela_procedimento.mostra_mensagem(
                "Procedimento não encontrado "
                "ou custo inválido!"
            )
            return

        atendimentos = (
            self.__controlador_sistema
            .controlador_atendimento.atendimentos
        )

        for atendimento in atendimentos:
            qtd = sum(
                1 for p in atendimento.procedimentos
                if p is proc
            )

            novo_total = (
                atendimento.valor_total
                + qtd * (novo_custo - proc.custo)
            )

            if (
                novo_total + 1e-9
                < atendimento.total_pago()
            ):
                self.__tela_procedimento.mostra_mensagem(
                    "Novo custo deixaria pagamento "
                    "maior que o total devido!"
                )
                return

        proc.custo = novo_custo

        self.__tela_procedimento.mostra_mensagem(
            "Custo alterado!"
        )

    def altera_profissional(
        self, descricao: str, novo_profissional
    ):
        proc = self.busca_procedimento(
            descricao
        )

        if proc is None or novo_profissional is None:
            self.__tela_procedimento.mostra_mensagem(
                "Procedimento ou profissional "
                "não encontrado!"
            )
            return

        proc.profissional = novo_profissional

        self.__tela_procedimento.mostra_mensagem(
            "Profissional alterado!"
        )

    def __cadastrar(self):
        dados = (
            self.__tela_procedimento
            .pega_dados_procedimento()
        )

        cpf = (
            self.__tela_procedimento
            .seleciona_profissional()
        )

        profissional = (
            self.__controlador_sistema
            .controlador_profissional
            .busca_profissional(cpf)
        )

        if profissional is None:
            self.__tela_procedimento.mostra_mensagem(
                "Profissional não encontrado!"
            )
            return

        self.cadastra_procedimento(
            Procedimento(
                dados["descricao"],
                dados["custo"],
                profissional
            )
        )

    def __excluir(self):
        descricao = (
            self.__tela_procedimento
            .seleciona_procedimento()
        )

        self.exclui_procedimento(descricao)

    def __editar(self, campo: str):
        descricao = (
            self.__tela_procedimento
            .seleciona_procedimento()
        )

        if campo == "custo":
            self.altera_custo(
                descricao,
                self.__tela_procedimento.pega_custo()
            )

        elif campo == "profissional":
            cpf = (
                self.__tela_procedimento
                .seleciona_profissional()
            )

            profissional = (
                self.__controlador_sistema
                .controlador_profissional
                .busca_profissional(cpf)
            )

            self.altera_profissional(
                descricao, profissional
            )

        else:
            nova = (
                self.__tela_procedimento
                .pega_novo_dado("descrição")
            )

            self.altera_descricao(
                descricao, nova
            )

    def __listar(self):
        if not self.__procedimentos:
            self.__tela_procedimento.mostra_mensagem(
                "Nenhum procedimento cadastrado."
            )

        for proc in self.__procedimentos:
            self.__tela_procedimento.mostra_procedimento({
                "descricao": proc.descricao,
                "custo": proc.custo,
                "profissional": proc.profissional.nome
            })

    def retorna(self):
        pass

    def abre_tela(self):
        opcoes = {
            1: self.__cadastrar,
            2: self.__excluir,
            3: lambda: self.__editar("descricao"),
            4: lambda: self.__editar("custo"),
            5: lambda: self.__editar("profissional"),
            6: self.__listar,
            0: self.retorna
        }

        while True:
            opcao = (
                self.__tela_procedimento
                .tela_opcoes()
            )

            if opcao not in opcoes:
                self.__tela_procedimento.mostra_mensagem(
                    "Opção inválida!"
                )
                continue

            opcoes[opcao]()

            if opcao == 0:
                break
