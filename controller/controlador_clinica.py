
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

    def busca_clinica(self, nome: str):
        return next(
            (c for c in self.__clinicas if c.nome == nome),
            None
        )

    def cadastra_clinica(
        self, clinica: Clinica
    ) -> None:
        if (
            not isinstance(clinica, Clinica)
            or not clinica.nome.strip()
            or not clinica.cidade.strip()
        ):
            self.__tela_clinica.mostra_mensagem(
                "Nome e cidade são obrigatórios!"
            )

        elif self.busca_clinica(clinica.nome):
            self.__tela_clinica.mostra_mensagem(
                "Já existe uma clínica com esse nome!"
            )

        elif (
            clinica.horario_abertura
            >= clinica.horario_fechamento
        ):
            self.__tela_clinica.mostra_mensagem(
                "Expediente inválido!"
            )

        else:
            self.__clinicas.append(clinica)
            self.__tela_clinica.mostra_mensagem(
                "Clínica cadastrada com sucesso!"
            )

    def exclui_clinica(self, nome: str) -> None:
        clinica = self.busca_clinica(nome)

        if clinica is None:
            self.__tela_clinica.mostra_mensagem(
                "Clínica não encontrada!"
            )

        elif clinica.atendimentos:
            self.__tela_clinica.mostra_mensagem(
                "Cancele os atendimentos da clínica "
                "antes da exclusão!"
            )

        else:
            self.__clinicas.remove(clinica)
            self.__tela_clinica.mostra_mensagem(
                "Clínica excluída com sucesso!"
            )

    def altera_horario(
        self, clinica: Clinica,
        abertura: time, fechamento: time
    ) -> None:
        if (
            clinica not in self.__clinicas
            or abertura >= fechamento
        ):
            self.__tela_clinica.mostra_mensagem(
                "Clínica ou expediente inválido!"
            )

        elif any(
            not (
                abertura <= a.hora_inicio
                < a.hora_fim <= fechamento
            )
            for a in clinica.atendimentos
        ):
            self.__tela_clinica.mostra_mensagem(
                "O novo horário excluiria "
                "atendimentos já marcados!"
            )

        else:
            clinica.horario_abertura = abertura
            clinica.horario_fechamento = fechamento

            self.__tela_clinica.mostra_mensagem(
                "Horário alterado com sucesso!"
            )

    def clinicas_abertas(self, hora: time) -> list:
        return [
            c for c in self.__clinicas
            if c.esta_aberta_clinica(hora)
        ]

    def altera_nome(
        self, nome_atual: str, novo_nome: str
    ):
        clinica = self.busca_clinica(nome_atual)

        if clinica is None or not novo_nome.strip():
            self.__tela_clinica.mostra_mensagem(
                "Clínica não encontrada ou nome inválido!"
            )

        elif self.busca_clinica(
            novo_nome
        ) not in (None, clinica):
            self.__tela_clinica.mostra_mensagem(
                "Nome já utilizado!"
            )

        else:
            clinica.nome = novo_nome
            self.__tela_clinica.mostra_mensagem(
                "Nome alterado!"
            )

    def altera_cidade(
        self, nome: str, nova_cidade: str
    ):
        self.__altera_texto(
            nome, "cidade", nova_cidade
        )

    def altera_descricao(
        self, nome: str, nova_descricao: str
    ):
        self.__altera_texto(
            nome, "descricao", nova_descricao
        )

    def __altera_texto(
        self, nome: str, campo: str, valor: str
    ):
        clinica = self.busca_clinica(nome)

        if clinica is None or not valor.strip():
            self.__tela_clinica.mostra_mensagem(
                "Clínica não encontrada ou valor vazio!"
            )
            return

        setattr(clinica, campo, valor)

        self.__tela_clinica.mostra_mensagem(
            "Dado alterado com sucesso!"
        )

    def __exibe(self, clinicas: list):
        if not clinicas:
            self.__tela_clinica.mostra_mensagem(
                "Nenhuma clínica encontrada!"
            )

        for c in clinicas:
            self.__tela_clinica.mostra_clinica({
                "nome": c.nome,
                "cidade": c.cidade,
                "descricao": c.descricao,
                "abertura": c.horario_abertura,
                "fechamento": c.horario_fechamento
            })

    def __cadastrar(self):
        dados = (
            self.__tela_clinica.pega_dados_clinica()
        )

        self.cadastra_clinica(
            Clinica(
                dados["nome"],
                dados["cidade"],
                dados["descricao"],
                dados["abertura"],
                dados["fechamento"]
            )
        )

    def __excluir(self):
        self.exclui_clinica(
            self.__tela_clinica.seleciona_clinica()
        )

    def __alterar_horarios(self):
        clinica = self.busca_clinica(
            self.__tela_clinica.seleciona_clinica()
        )

        if clinica is None:
            self.__tela_clinica.mostra_mensagem(
                "Clínica não encontrada!"
            )
            return

        dados = (
            self.__tela_clinica.pega_novos_horarios()
        )

        self.altera_horario(
            clinica,
            dados["abertura"],
            dados["fechamento"]
        )

    def __listar_abertas(self):
        hora = self.__tela_clinica.pega_horario(
            "Horário de consulta"
        )

        self.__exibe(
            self.clinicas_abertas(hora)
        )

    def __editar(self, campo: str):
        nome = (
            self.__tela_clinica.seleciona_clinica()
        )

        valor = self.__tela_clinica.pega_novo_dado(
            campo
        )

        {
            "nome": self.altera_nome,
            "cidade": self.altera_cidade,
            "descricao": self.altera_descricao
        }[campo](nome, valor)

    def retorna(self):
        pass

    def abre_tela(self):
        opcoes = {
            1: self.__cadastrar,
            2: self.__excluir,
            3: self.__alterar_horarios,
            4: self.__listar_abertas,
            5: lambda: self.__exibe(self.__clinicas),
            6: lambda: self.__editar("nome"),
            7: lambda: self.__editar("cidade"),
            8: lambda: self.__editar("descricao"),
            0: self.retorna
        }

        while True:
            opcao = self.__tela_clinica.tela_opcoes()

            if opcao not in opcoes:
                self.__tela_clinica.mostra_mensagem(
                    "Opção inválida!"
                )
                continue

            opcoes[opcao]()

            if opcao == 0:
                break
