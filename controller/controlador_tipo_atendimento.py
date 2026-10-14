
from model.tipoatendimento import TipoAtendimento
from view.tela_tipo_atendimento import TelaTipoAtendimento


class ControladorTipoAtendimento:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_tipo_atendimento = TelaTipoAtendimento()
        self.__tipos_atendimento = []

    @property
    def tipos_atendimento(self) -> list:
        return self.__tipos_atendimento

    def cadastra_tipo_atendimento(
        self, tipo_atendimento: TipoAtendimento
    ) -> None:
        if isinstance(tipo_atendimento, TipoAtendimento):
            if self.busca_tipo_atendimento(
                tipo_atendimento.codigo
            ) is None:
                self.__tipos_atendimento.append(
                    tipo_atendimento
                )

                self.__tela_tipo_atendimento.mostra_mensagem(
                    "Tipo de atendimento cadastrado com sucesso!"
                )

            else:
                self.__tela_tipo_atendimento.mostra_mensagem(
                    "Já existe um tipo de atendimento com este código!"
                )

    def exclui_tipo_atendimento(
        self, codigo: int
    ) -> None:
        tipo = self.busca_tipo_atendimento(codigo)

        if tipo is not None:
            atendimentos = (
                self.__controlador_sistema
                .controlador_atendimento.atendimentos
            )

            if any(
                a.tipo_atendimento is tipo
                for a in atendimentos
            ):
                self.__tela_tipo_atendimento.mostra_mensagem(
                    "Tipo utilizado em atendimentos! Não pode excluir."
                )
                return

            self.__tipos_atendimento.remove(tipo)

            self.__tela_tipo_atendimento.mostra_mensagem(
                "Tipo de atendimento excluído com sucesso!"
            )

        else:
            self.__tela_tipo_atendimento.mostra_mensagem(
                "Tipo de atendimento não encontrado!"
            )

    def altera_tipo_atendimento(
        self, codigo: int, novo_nome: str
    ) -> None:
        tipo = self.busca_tipo_atendimento(codigo)

        if tipo is not None:
            tipo.nome = novo_nome

            self.__tela_tipo_atendimento.mostra_mensagem(
                "Tipo de atendimento alterado com sucesso!"
            )

        else:
            self.__tela_tipo_atendimento.mostra_mensagem(
                "Tipo de atendimento não encontrado!"
            )

    def busca_tipo_atendimento(
        self, codigo: int
    ) -> TipoAtendimento:
        for tipo in self.__tipos_atendimento:
            if tipo.codigo == codigo:
                return tipo

        return None

    def retorna(self) -> None:
        pass

    def abre_tela(self) -> None:
        lista_opcoes = {
            1: self.__incluir,
            2: self.__alterar,
            3: self.__listar,
            4: self.__excluir,
            0: self.retorna
        }

        while True:
            opcao_escolhida = (
                self.__tela_tipo_atendimento
                .tela_opcoes()
            )

            funcao_escolhida = lista_opcoes.get(
                opcao_escolhida
            )

            if funcao_escolhida:
                funcao_escolhida()

                if opcao_escolhida == 0:
                    break

            else:
                self.__tela_tipo_atendimento.mostra_mensagem(
                    "Opção inválida! Escolha um número do menu."
                )

    def __incluir(self) -> None:
        dados = (
            self.__tela_tipo_atendimento
            .pega_dados_tipo()
        )

        if dados and dados["nome"]:
            novo_tipo = TipoAtendimento(
                dados["codigo"], dados["nome"]
            )

            self.cadastra_tipo_atendimento(
                novo_tipo
            )

        else:
            self.__tela_tipo_atendimento.mostra_mensagem(
                "O nome não pode ser vazio!"
            )

    def __alterar(self) -> None:
        self.__listar()

        if not self.__tipos_atendimento:
            return

        codigo = (
            self.__tela_tipo_atendimento
            .seleciona_tipo()
        )

        if self.busca_tipo_atendimento(codigo) is None:
            self.__tela_tipo_atendimento.mostra_mensagem(
                "Tipo de atendimento não encontrado!"
            )
            return

        novo_nome = (
            self.__tela_tipo_atendimento.pega_novo_dado(
                "nome do tipo de atendimento"
            )
        )

        if novo_nome:
            self.altera_tipo_atendimento(
                codigo, novo_nome
            )

        else:
            self.__tela_tipo_atendimento.mostra_mensagem(
                "O nome não pode ser vazio!"
            )

    def __listar(self) -> None:
        if not self.__tipos_atendimento:
            self.__tela_tipo_atendimento.mostra_mensagem(
                "Nenhum tipo de atendimento cadastrado."
            )
            return

        self.__tela_tipo_atendimento.mostra_mensagem(
            "LISTA DE TIPOS DE ATENDIMENTO"
        )

        for tipo in self.__tipos_atendimento:
            self.__tela_tipo_atendimento.mostra_tipo({
                "codigo": tipo.codigo,
                "nome": tipo.nome
            })

    def __excluir(self) -> None:
        self.__listar()

        if not self.__tipos_atendimento:
            return

        codigo = (
            self.__tela_tipo_atendimento
            .seleciona_tipo()
        )

        self.exclui_tipo_atendimento(codigo)
