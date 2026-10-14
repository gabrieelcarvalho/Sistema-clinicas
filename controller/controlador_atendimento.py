
from datetime import date as Date, time as Time
from model.atendimento import Atendimento
from model.paciente import Paciente
from model.acompanhante import Acompanhante
from model.pagamento import Pagamento
from model.pagamentodinheiro import PagamentoDinheiro
from model.pagamentopix import PagamentoPix
from model.pagamentocartao import PagamentoCartao
from model.procedimento import Procedimento
from view.tela_atendimento import TelaAtendimento
from excecoes import (
    ErroSistemaClinicas,
    DadosInvalidosError,
    RegistroNaoEncontradoError,
    PacienteMenorDesacompanhadoError,
    HorarioInvalidoError,
    AtendimentoForaDoHorarioError,
    ConflitoDeHorarioError,
    PagamentoForaDoPrazoError,
    ValorPagamentoInvalidoError,
    PagamentoExcedenteError,
    PagamentoDeOutroAtendimentoError,
    ModalidadePagamentoInvalidaError
)


class ControladorAtendimento:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_atendimento = TelaAtendimento()
        self.__atendimentos = []

    @property
    def atendimentos(self) -> list:
        return self.__atendimentos

    def busca_atendimento(self, numero_atendimento: int):
        return next(
            (
                a for a in self.__atendimentos
                if a.numero_atendimento == numero_atendimento
            ),
            None
        )

    def valida_maioridade(
        self, paciente: Paciente,
        acomp: Acompanhante,
        data_referencia: Date = None
    ) -> bool:
        return (
            paciente.maior_de_idade(data_referencia)
            or acomp is not None
        )

    def valida_horario(
        self, clinica, ini: Time, fim: Time
    ) -> bool:
        return clinica.esta_aberta_clinica(ini, fim)

    def __confere_conflito(
        self, profissional, data: Date,
        inicio: Time, fim: Time, ignorar=None
    ) -> None:
        for atual in self.__atendimentos:
            if atual is ignorar:
                continue

            if (
                atual.profissional is profissional
                and atual.data == data
                and inicio < atual.hora_fim
                and fim > atual.hora_inicio
            ):
                raise ConflitoDeHorarioError()

    def __valida_agendamento(
        self, atendimento: Atendimento
    ) -> None:
        if not isinstance(atendimento, Atendimento):
            raise DadosInvalidosError(
                "Atendimento inválido!"
            )

        if not 0 <= atendimento.valor < float("inf"):
            raise DadosInvalidosError(
                "Valor do atendimento inválido!"
            )

        if not self.valida_maioridade(
            atendimento.paciente,
            atendimento.acompanhante,
            atendimento.data
        ):
            raise PacienteMenorDesacompanhadoError()

        if atendimento.hora_inicio >= atendimento.hora_fim:
            raise HorarioInvalidoError()

        if not self.valida_horario(
            atendimento.clinica,
            atendimento.hora_inicio,
            atendimento.hora_fim
        ):
            raise AtendimentoForaDoHorarioError()

        self.__confere_conflito(
            atendimento.profissional,
            atendimento.data,
            atendimento.hora_inicio,
            atendimento.hora_fim,
            ignorar=atendimento
        )

    def agenda_atendimento(
        self, atendimento: Atendimento
    ) -> None:
        try:
            if not isinstance(atendimento, Atendimento):
                raise DadosInvalidosError(
                    "Atendimento inválido!"
                )

            if self.busca_atendimento(
                atendimento.numero_atendimento
            ):
                raise DadosInvalidosError(
                    "Número de atendimento já utilizado!"
                )

            self.__valida_agendamento(atendimento)

            self.__atendimentos.append(atendimento)

            atendimento.clinica.registra_atendimento(
                atendimento
            )

            atendimento.clinica.inclui_paciente(
                atendimento.paciente
            )

            atendimento.clinica.inclui_profissional(
                atendimento.profissional
            )

            self.__tela_atendimento.mostra_mensagem(
                "Atendimento agendado com sucesso!"
            )

        except ErroSistemaClinicas as erro:
            self.__tela_atendimento.mostra_mensagem(
                str(erro)
            )

    def cancela_atendimento(
        self, numero_atendimento: int
    ) -> None:
        atendimento = self.busca_atendimento(
            numero_atendimento
        )

        if atendimento is None:
            self.__tela_atendimento.mostra_mensagem(
                "Atendimento não encontrado!"
            )
            return

        self.__atendimentos.remove(atendimento)

        atendimento.clinica.cancela_atendimento(
            atendimento
        )

        if not any(
            a.clinica is atendimento.clinica
            and a.paciente is atendimento.paciente
            for a in self.__atendimentos
        ):
            atendimento.clinica.exclui_paciente(
                atendimento.paciente
            )

        if not any(
            a.clinica is atendimento.clinica
            and a.profissional is atendimento.profissional
            for a in self.__atendimentos
        ):
            atendimento.clinica.exclui_profissional(
                atendimento.profissional
            )

        self.__tela_atendimento.mostra_mensagem(
            "Atendimento cancelado com sucesso!"
        )

    def reagenda_atendimento(
        self, numero_atendimento: int,
        hora_inicio: Time, hora_fim: Time,
        data: Date
    ) -> None:
        try:
            atendimento = self.busca_atendimento(
                numero_atendimento
            )

            if atendimento is None:
                raise RegistroNaoEncontradoError(
                    "Atendimento não encontrado!"
                )

            if hora_inicio >= hora_fim:
                raise HorarioInvalidoError()

            if not self.valida_horario(
                atendimento.clinica,
                hora_inicio,
                hora_fim
            ):
                raise AtendimentoForaDoHorarioError()

            if not self.valida_maioridade(
                atendimento.paciente,
                atendimento.acompanhante,
                data
            ):
                raise PacienteMenorDesacompanhadoError()

            if any(
                pagamento.data > data
                for pagamento in atendimento.pagamentos
            ):
                raise PagamentoForaDoPrazoError(
                    "Há pagamentos posteriores à nova data!"
                )

            self.__confere_conflito(
                atendimento.profissional,
                data,
                hora_inicio,
                hora_fim,
                ignorar=atendimento
            )

            atendimento.data = data
            atendimento.hora_inicio = hora_inicio
            atendimento.hora_fim = hora_fim

            self.__tela_atendimento.mostra_mensagem(
                "Atendimento reagendado com sucesso!"
            )

        except ErroSistemaClinicas as erro:
            self.__tela_atendimento.mostra_mensagem(
                str(erro)
            )

    def altera_atendimento(
        self, numero_atendimento: int, dados: dict
    ) -> None:
        try:
            atendimento = self.busca_atendimento(
                numero_atendimento
            )

            if atendimento is None:
                raise RegistroNaoEncontradoError(
                    "Atendimento não encontrado!"
                )

            profissional = (
                dados.get("profissional")
                or atendimento.profissional
            )

            tipo = (
                dados.get("tipo_atendimento")
                or atendimento.tipo_atendimento
            )

            valor = (
                atendimento.valor
                if dados.get("valor") is None
                else dados["valor"]
            )

            if not 0 <= valor < float("inf"):
                raise DadosInvalidosError(
                    "Valor inválido!"
                )

            total = valor + sum(
                p.custo
                for p in atendimento.procedimentos
            )

            if total + 1e-9 < atendimento.total_pago():
                raise PagamentoExcedenteError(
                    "O novo valor é inferior ao total já pago!"
                )

            self.__confere_conflito(
                profissional,
                atendimento.data,
                atendimento.hora_inicio,
                atendimento.hora_fim,
                ignorar=atendimento
            )

            anterior = atendimento.profissional

            atendimento.profissional = profissional
            atendimento.tipo_atendimento = tipo
            atendimento.valor = valor

            if anterior is not profissional:
                atendimento.clinica.inclui_profissional(
                    profissional
                )

                if not any(
                    a.clinica is atendimento.clinica
                    and a.profissional is anterior
                    for a in self.__atendimentos
                ):
                    atendimento.clinica.exclui_profissional(
                        anterior
                    )

            self.__tela_atendimento.mostra_mensagem(
                "Atendimento alterado com sucesso!"
            )

        except ErroSistemaClinicas as erro:
            self.__tela_atendimento.mostra_mensagem(
                str(erro)
            )

    def inclui_procedimento(
        self, numero_atendimento: int,
        procedimento: Procedimento
    ) -> None:
        atendimento = self.busca_atendimento(
            numero_atendimento
        )

        if (
            atendimento is None
            or not isinstance(procedimento, Procedimento)
        ):
            self.__tela_atendimento.mostra_mensagem(
                "Atendimento ou procedimento inválido!"
            )
            return

        atendimento.inclui_procedimento(
            procedimento
        )

        self.__tela_atendimento.mostra_mensagem(
            "Procedimento incluído com sucesso!"
        )

    def exclui_procedimento_atendimento(
        self, numero_atendimento: int, indice: int
    ) -> None:
        atendimento = self.busca_atendimento(
            numero_atendimento
        )

        if (
            atendimento is None
            or not 0 <= indice < len(atendimento.procedimentos)
        ):
            self.__tela_atendimento.mostra_mensagem(
                "Procedimento não encontrado!"
            )
            return

        procedimento = atendimento.procedimentos[indice]

        if (
            atendimento.total_pago()
            > atendimento.valor_total - procedimento.custo + 1e-9
        ):
            self.__tela_atendimento.mostra_mensagem(
                "Exclusão deixaria total pago maior "
                "que o valor do atendimento!"
            )
            return

        atendimento.procedimentos.pop(indice)

        self.__tela_atendimento.mostra_mensagem(
            "Procedimento removido do atendimento!"
        )

    def __valida_pagamento(
        self, atendimento, pagamento: Pagamento
    ) -> None:
        if not isinstance(pagamento, Pagamento):
            raise DadosInvalidosError(
                "Objeto de pagamento inválido!"
            )

        if pagamento.atendimento is not atendimento:
            raise PagamentoDeOutroAtendimentoError()

        if pagamento.data > atendimento.data:
            raise PagamentoForaDoPrazoError()

        if not 0 < pagamento.valor_pagamento < float("inf"):
            raise ValorPagamentoInvalidoError()

        if isinstance(pagamento, PagamentoPix):
            if not pagamento.cpf.strip():
                raise DadosInvalidosError(
                    "Informe o CPF do pagador!"
                )

        if isinstance(pagamento, PagamentoCartao):
            if (
                pagamento.parcelas < 1
                or not pagamento.numero.strip()
                or not pagamento.bandeira.strip()
            ):
                raise DadosInvalidosError(
                    "Número, bandeira e parcelas "
                    "do cartão são obrigatórios!"
                )

    def registra_pagamento(
        self, numero_atendimento: int,
        pagamento: Pagamento
    ) -> None:
        try:
            atendimento = self.busca_atendimento(
                numero_atendimento
            )

            if atendimento is None:
                raise RegistroNaoEncontradoError(
                    "Atendimento não encontrado!"
                )

            self.__valida_pagamento(
                atendimento, pagamento
            )

            if (
                pagamento.valor_pagamento
                > atendimento.mostra_valor_restante() + 1e-9
            ):
                raise PagamentoExcedenteError()

            atendimento.adiciona_pagamento(
                pagamento
            )

            self.__tela_atendimento.mostra_mensagem(
                "Pagamento registrado com sucesso!"
            )

        except ErroSistemaClinicas as erro:
            self.__tela_atendimento.mostra_mensagem(
                str(erro)
            )

    def lista_pagamentos(
        self, numero_atendimento: int
    ) -> list:
        atendimento = self.busca_atendimento(
            numero_atendimento
        )

        return (
            list(atendimento.pagamentos)
            if atendimento is not None
            else []
        )

    def exclui_pagamento(
        self, numero_atendimento: int, indice: int
    ) -> None:
        atendimento = self.busca_atendimento(
            numero_atendimento
        )

        if (
            atendimento is None
            or not 0 <= indice < len(atendimento.pagamentos)
        ):
            self.__tela_atendimento.mostra_mensagem(
                "Pagamento não encontrado!"
            )
            return

        atendimento.pagamentos.pop(indice)

        self.__tela_atendimento.mostra_mensagem(
            "Pagamento excluído com sucesso!"
        )

    def altera_pagamento(
        self, numero_atendimento: int,
        indice: int, novo_pagamento: Pagamento
    ) -> None:
        try:
            atendimento = self.busca_atendimento(
                numero_atendimento
            )

            if (
                atendimento is None
                or not 0 <= indice < len(atendimento.pagamentos)
            ):
                raise RegistroNaoEncontradoError(
                    "Pagamento não encontrado!"
                )

            self.__valida_pagamento(
                atendimento, novo_pagamento
            )

            total_outros = sum(
                p.valor_pagamento
                for i, p in enumerate(atendimento.pagamentos)
                if i != indice
            )

            if (
                total_outros + novo_pagamento.valor_pagamento
                > atendimento.valor_total + 1e-9
            ):
                raise PagamentoExcedenteError()

            atendimento.pagamentos[indice] = novo_pagamento

            self.__tela_atendimento.mostra_mensagem(
                "Pagamento alterado com sucesso!"
            )

        except ErroSistemaClinicas as erro:
            self.__tela_atendimento.mostra_mensagem(
                str(erro)
            )

    def __cria_pagamento(self, atendimento):
        modalidade = (
            self.__tela_atendimento
            .seleciona_forma_pagamento()
        )

        if modalidade == 1:
            dados = (
                self.__tela_atendimento
                .pega_dados_dinheiro()
            )

            return PagamentoDinheiro(
                dados["data"],
                atendimento,
                dados["valor_pagamento"]
            )

        if modalidade == 2:
            dados = (
                self.__tela_atendimento
                .pega_dados_pix()
            )

            return PagamentoPix(
                dados["data"],
                atendimento,
                dados["valor_pagamento"],
                dados["cpf"]
            )

        if modalidade == 3:
            dados = (
                self.__tela_atendimento
                .pega_dados_cartao()
            )

            return PagamentoCartao(
                dados["data"],
                atendimento,
                dados["valor_pagamento"],
                dados["bandeira"],
                dados["numero"],
                dados["parcelas"]
            )

        raise ModalidadePagamentoInvalidaError()

    def __agendar(self):
        dados = (
            self.__tela_atendimento
            .pega_dados_agendamento()
        )

        sistema = self.__controlador_sistema

        clinica = (
            sistema.controlador_clinica.busca_clinica(
                dados["nome_clinica"]
            )
        )

        paciente = (
            sistema.controlador_paciente.busca_paciente(
                dados["cpf_paciente"]
            )
        )

        profissional = (
            sistema.controlador_profissional.busca_profissional(
                dados["cpf_profissional"]
            )
        )

        tipo = (
            sistema.controlador_tipo_atendimento
            .busca_tipo_atendimento(
                dados["codigo_tipo"]
            )
        )

        if None in (
            clinica, paciente, profissional, tipo
        ):
            self.__tela_atendimento.mostra_mensagem(
                "Clínica, paciente, profissional "
                "ou tipo não encontrado!"
            )
            return

        acompanhante = None

        if not paciente.maior_de_idade(dados["data"]):
            self.__tela_atendimento.mostra_mensagem(
                "Informe o acompanhante do "
                "paciente menor de idade."
            )

            acompanhante = Acompanhante(
                **self.__tela_atendimento
                .pega_dados_acompanhante()
            )

        atendimento = Atendimento(
            clinica,
            paciente,
            profissional,
            dados["data"],
            dados["hora_inicio"],
            dados["hora_fim"],
            tipo,
            dados["valor"],
            dados["numero_atendimento"],
            acompanhante
        )

        self.agenda_atendimento(atendimento)

    def __reagendar(self):
        numero = (
            self.__tela_atendimento
            .seleciona_atendimento()
        )

        dados = (
            self.__tela_atendimento
            .pega_dados_reagendamento()
        )

        self.reagenda_atendimento(
            numero,
            dados["hora_inicio"],
            dados["hora_fim"],
            dados["data"]
        )

    def __alterar_dados(self):
        numero = (
            self.__tela_atendimento
            .seleciona_atendimento()
        )

        if self.busca_atendimento(numero) is None:
            self.__tela_atendimento.mostra_mensagem(
                "Atendimento não encontrado!"
            )
            return

        dados = (
            self.__tela_atendimento
            .pega_dados_alteracao()
        )

        atualizacoes = {
            "valor": dados["valor"]
        }

        if dados["cpf_profissional"]:
            profissional = (
                self.__controlador_sistema
                .controlador_profissional
                .busca_profissional(
                    dados["cpf_profissional"]
                )
            )

            if profissional is None:
                self.__tela_atendimento.mostra_mensagem(
                    "Profissional não encontrado!"
                )
                return

            atualizacoes["profissional"] = profissional

        if dados["codigo_tipo"] is not None:
            tipo = (
                self.__controlador_sistema
                .controlador_tipo_atendimento
                .busca_tipo_atendimento(
                    dados["codigo_tipo"]
                )
            )

            if tipo is None:
                self.__tela_atendimento.mostra_mensagem(
                    "Tipo não encontrado!"
                )
                return

            atualizacoes["tipo_atendimento"] = tipo

        self.altera_atendimento(
            numero, atualizacoes
        )

    def __cancelar(self):
        numero = (
            self.__tela_atendimento
            .seleciona_atendimento()
        )

        self.cancela_atendimento(numero)

    def __incluir_proc(self):
        numero = (
            self.__tela_atendimento
            .seleciona_atendimento()
        )

        descricao = (
            self.__tela_atendimento
            .seleciona_procedimento()
        )

        proc = (
            self.__controlador_sistema
            .controlador_procedimento
            .busca_procedimento(descricao)
        )

        self.inclui_procedimento(
            numero, proc
        )

    def __pagar(self):
        numero = (
            self.__tela_atendimento
            .seleciona_atendimento()
        )

        atendimento = self.busca_atendimento(
            numero
        )

        if atendimento is None:
            self.__tela_atendimento.mostra_mensagem(
                "Atendimento não encontrado!"
            )
            return

        pagamento = self.__cria_pagamento(atendimento)

        self.registra_pagamento(
            numero, pagamento
        )

    def __listar_pagamentos(self):
        numero = (
            self.__tela_atendimento
            .seleciona_atendimento()
        )

        if self.busca_atendimento(numero) is None:
            self.__tela_atendimento.mostra_mensagem(
                "Atendimento não encontrado!"
            )
            return

        pagamentos = self.lista_pagamentos(numero)

        self.__tela_atendimento.mostra_pagamentos(
            [
                p.mostra_dados()
                for p in pagamentos
            ]
        )

    def __alterar_pagamento(self):
        numero = (
            self.__tela_atendimento
            .seleciona_atendimento()
        )

        atendimento = self.busca_atendimento(
            numero
        )

        if (
            atendimento is None
            or not atendimento.pagamentos
        ):
            self.__tela_atendimento.mostra_mensagem(
                "Atendimento sem pagamentos!"
            )
            return

        self.__tela_atendimento.mostra_pagamentos(
            [
                p.mostra_dados()
                for p in atendimento.pagamentos
            ]
        )

        indice = (
            self.__tela_atendimento.seleciona_indice(
                "Número do pagamento"
            )
        )

        if not 0 <= indice < len(atendimento.pagamentos):
            self.__tela_atendimento.mostra_mensagem(
                "Pagamento não encontrado!"
            )
            return

        novo_pagamento = self.__cria_pagamento(
            atendimento
        )

        self.altera_pagamento(
            numero,
            indice,
            novo_pagamento
        )

    def __excluir_pagamento(self):
        numero = (
            self.__tela_atendimento
            .seleciona_atendimento()
        )

        pagamentos = self.lista_pagamentos(numero)

        if not pagamentos:
            self.__tela_atendimento.mostra_mensagem(
                "Nenhum pagamento encontrado!"
            )
            return

        self.__tela_atendimento.mostra_pagamentos(
            [
                p.mostra_dados()
                for p in pagamentos
            ]
        )

        indice = (
            self.__tela_atendimento.seleciona_indice(
                "Número do pagamento"
            )
        )

        self.exclui_pagamento(
            numero, indice
        )

    def __listar_procedimentos(self):
        numero = (
            self.__tela_atendimento
            .seleciona_atendimento()
        )

        atendimento = self.busca_atendimento(
            numero
        )

        if atendimento is None:
            self.__tela_atendimento.mostra_mensagem(
                "Atendimento não encontrado!"
            )
            return

        self.__tela_atendimento.mostra_procedimentos(
            [
                p.mostra_dados()
                for p in atendimento.procedimentos
            ]
        )

    def __excluir_procedimento(self):
        numero = (
            self.__tela_atendimento
            .seleciona_atendimento()
        )

        atendimento = self.busca_atendimento(
            numero
        )

        if (
            atendimento is None
            or not atendimento.procedimentos
        ):
            self.__tela_atendimento.mostra_mensagem(
                "Atendimento sem procedimentos!"
            )
            return

        self.__tela_atendimento.mostra_procedimentos(
            [
                p.mostra_dados()
                for p in atendimento.procedimentos
            ]
        )

        indice = (
            self.__tela_atendimento.seleciona_indice(
                "Número do procedimento"
            )
        )

        self.exclui_procedimento_atendimento(
            numero, indice
        )

    def __listar(self):
        if not self.__atendimentos:
            self.__tela_atendimento.mostra_mensagem(
                "Nenhum atendimento cadastrado."
            )
            return

        for a in self.__atendimentos:
            self.__tela_atendimento.mostra_atendimento({
                "numero_atendimento": a.numero_atendimento,
                "clinica": a.clinica.nome,
                "paciente": a.paciente.nome,
                "profissional": a.profissional.nome,
                "data": a.data.strftime("%d/%m/%Y"),
                "hora_inicio": a.hora_inicio.strftime("%H:%M"),
                "hora_fim": a.hora_fim.strftime("%H:%M"),
                "tipo": a.tipo_atendimento.nome,
                "valor_total": a.valor_total,
                "valor_restante": a.mostra_valor_restante(),
                "pago": "Sim" if a.pago() else "Não"
            })

    def retorna(self):
        pass

    def abre_tela(self):
        opcoes = {
            1: self.__agendar,
            2: self.__reagendar,
            3: self.__cancelar,
            4: self.__incluir_proc,
            5: self.__pagar,
            6: self.__listar,
            7: self.__listar_pagamentos,
            8: self.__alterar_pagamento,
            9: self.__excluir_pagamento,
            10: self.__listar_procedimentos,
            11: self.__excluir_procedimento,
            12: self.__alterar_dados,
            0: self.retorna
        }

        while True:
            try:
                opcao = (
                    self.__tela_atendimento
                    .tela_opcoes()
                )

                if opcao not in opcoes:
                    self.__tela_atendimento.mostra_mensagem(
                        "Opção inválida!"
                    )
                    continue

                opcoes[opcao]()

                if opcao == 0:
                    break

            except ErroSistemaClinicas as erro:
                self.__tela_atendimento.mostra_mensagem(
                    str(erro)
                )
