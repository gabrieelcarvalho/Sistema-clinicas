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

from exceptions.clinica_nao_cadastrada_exception import ClinicaNaoCadastradaException
from exceptions.paciente_nao_cadastrado_exception import PacienteNaoCadastradoException
from exceptions.profissional_nao_cadastrado_exception import ProfissionalNaoCadastradoException
from exceptions.tipo_atendimento_nao_cadastrado_exception import TipoAtendimentoNaoCadastradoException
from exceptions.acompanhante_menor_exception import AcompanhanteMenorDeIdadeException


class ControladorAtendimento:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_atendimento = TelaAtendimento()
        self.__atendimentos = []
        self.__proximo_numero = 1

    @property
    def atendimentos(self) -> list:
        return self.__atendimentos

    def busca_atendimento(self, numero_atendimento: int) -> Atendimento:
        return next(
            (a for a in self.__atendimentos if a.numero_atendimento == numero_atendimento),
            None
        )

    def valida_maioridade(
        self,
        paciente: Paciente,
        acomp: Acompanhante,
        data_referencia: Date
    ) -> bool:
        if acomp is not None:
            nascimento = acomp.data_nascimento
            idade = data_referencia.year - nascimento.year

            if (data_referencia.month, data_referencia.day) < (nascimento.month, nascimento.day):
                idade -= 1

            if idade < 18:
                raise AcompanhanteMenorDeIdadeException()

        return paciente.maior_de_idade(data_referencia) or acomp is not None

    def valida_horario(self, clinica, ini: Time, fim: Time) -> bool:
        return clinica.esta_aberta_clinica(ini, fim)

    def agenda_atendimento(self, atendimento: Atendimento) -> None:
        if not isinstance(atendimento, Atendimento):
            self.__tela_atendimento.mostra_mensagem("Atendimento inválido!")
            return

        try:
            if not self.valida_maioridade(
                atendimento.paciente,
                atendimento.acompanhante,
                atendimento.data
            ):
                self.__tela_atendimento.mostra_mensagem(
                    "Paciente menor de idade precisa de acompanhante!"
                )
                return
        except AcompanhanteMenorDeIdadeException as erro:
            self.__tela_atendimento.mostra_mensagem(str(erro))
            return

        if self.busca_atendimento(atendimento.numero_atendimento) is not None:
            self.__tela_atendimento.mostra_mensagem("Número de atendimento já cadastrado!")
            return

        
        if not self.valida_horario(
            atendimento.clinica,
            atendimento.hora_inicio,
            atendimento.hora_fim
        ):
            self.__tela_atendimento.mostra_mensagem(
                "A clínica está fechada no horário solicitado!"
            )
            return

        self.__atendimentos.append(atendimento)
        atendimento.clinica.registra_atendimento(atendimento)
        atendimento.clinica.inclui_paciente(atendimento.paciente)
        atendimento.clinica.inclui_profissional(atendimento.profissional)

        self.__proximo_numero += 1
        self.__tela_atendimento.mostra_mensagem("Atendimento agendado com sucesso!")

    def cancela_atendimento(self, numero_atendimento: int) -> None:
        atendimento = self.busca_atendimento(numero_atendimento)
        if atendimento is None:
            self.__tela_atendimento.mostra_mensagem("Atendimento não encontrado!")
            return

        self.__atendimentos.remove(atendimento)
        atendimento.clinica.cancela_atendimento(atendimento)

        if not any(a.clinica is atendimento.clinica and a.paciente is atendimento.paciente for a in self.__atendimentos):
            atendimento.clinica.exclui_paciente(atendimento.paciente)

        if not any(a.clinica is atendimento.clinica and a.profissional is atendimento.profissional for a in self.__atendimentos):
            atendimento.clinica.exclui_profissional(atendimento.profissional)

        self.__tela_atendimento.mostra_mensagem("Atendimento cancelado com sucesso!")

    def reagenda_atendimento(self, numero_atendimento: int, hora_inicio: Time, hora_fim: Time, data: Date) -> None:
        atendimento = self.busca_atendimento(numero_atendimento)
        if atendimento is None:
            self.__tela_atendimento.mostra_mensagem("Atendimento não encontrado!")
            return

        if hora_inicio >= hora_fim:
            self.__tela_atendimento.mostra_mensagem("Horário final deve ser posterior ao inicial!")
            return

        if not self.valida_horario(atendimento.clinica, hora_inicio, hora_fim):
            self.__tela_atendimento.mostra_mensagem("Atendimento fora do horário de funcionamento da clínica!")
            return

        try:
            if not self.valida_maioridade(
                atendimento.paciente,
                atendimento.acompanhante,
                data
            ):
                self.__tela_atendimento.mostra_mensagem(
                    "Paciente menor de idade precisa de acompanhante!"
                )
                return
        except AcompanhanteMenorDeIdadeException as erro:
            self.__tela_atendimento.mostra_mensagem(str(erro))
            return

        atendimento.data = data
        atendimento.hora_inicio = hora_inicio
        atendimento.hora_fim = hora_fim
        self.__tela_atendimento.mostra_mensagem("Atendimento reagendado com sucesso!")

    def altera_atendimento(self, numero_atendimento: int, dados: dict) -> None:
        atendimento = self.busca_atendimento(numero_atendimento)
        if atendimento is None:
            self.__tela_atendimento.mostra_mensagem("Atendimento não encontrado!")
            return

        if "profissional" in dados and dados["profissional"] is not None:
            atendimento.profissional = dados["profissional"]

        if "tipo_atendimento" in dados and dados["tipo_atendimento"] is not None:
            atendimento.tipo_atendimento = dados["tipo_atendimento"]

        if "valor" in dados and dados["valor"] is not None:
            atendimento.valor = dados["valor"]

        self.__tela_atendimento.mostra_mensagem("Atendimento alterado com sucesso!")

    def inclui_procedimento(self, numero_atendimento: int, procedimento: Procedimento) -> None:
        atendimento = self.busca_atendimento(numero_atendimento)
        if atendimento is None or procedimento is None:
            self.__tela_atendimento.mostra_mensagem("Atendimento ou procedimento inválido!")
            return

        atendimento.inclui_procedimento(procedimento)
        self.__tela_atendimento.mostra_mensagem("Procedimento incluído com sucesso!")

    def exclui_procedimento_atendimento(self, numero_atendimento: int, procedimento: Procedimento) -> None:
        atendimento = self.busca_atendimento(numero_atendimento)
        if atendimento is None:
            self.__tela_atendimento.mostra_mensagem("Atendimento não encontrado!")
            return

        atendimento.remove_procedimento(procedimento)
        self.__tela_atendimento.mostra_mensagem("Procedimento removido com sucesso!")

    def lista_procedimentos_atendimento(self, numero_atendimento: int) -> list:
        atendimento = self.busca_atendimento(numero_atendimento)
        return list(atendimento.procedimentos) if atendimento else []

    def registra_pagamento(self, numero_atendimento: int, pagamento: Pagamento) -> None:
        atendimento = self.busca_atendimento(numero_atendimento)
        if atendimento is None:
            self.__tela_atendimento.mostra_mensagem("Atendimento não encontrado!")
            return

        atendimento.adiciona_pagamento(pagamento)
        self.__tela_atendimento.mostra_mensagem("Pagamento registrado com sucesso!")

    def lista_pagamentos(self, numero_atendimento: int) -> list:
        atendimento = self.busca_atendimento(numero_atendimento)
        return list(atendimento.pagamentos) if atendimento else []

    def exclui_pagamento(self, numero_atendimento: int, indice_pagamento: int) -> None:
        atendimento = self.busca_atendimento(numero_atendimento)
        if atendimento is None or not (0 <= indice_pagamento < len(atendimento.pagamentos)):
            self.__tela_atendimento.mostra_mensagem("Pagamento não encontrado!")
            return

        atendimento.pagamentos.pop(indice_pagamento)
        self.__tela_atendimento.mostra_mensagem("Pagamento excluído com sucesso!")

    def altera_pagamento(self, numero_atendimento: int, indice_pagamento: int, dados: dict) -> None:
        atendimento = self.busca_atendimento(numero_atendimento)
        if atendimento is None or not (0 <= indice_pagamento < len(atendimento.pagamentos)):
            self.__tela_atendimento.mostra_mensagem("Pagamento não encontrado!")
            return

        pagamento = atendimento.pagamentos[indice_pagamento]
        if "valor" in dados and dados["valor"] is not None:
            pagamento.valor_pagamento = dados["valor"]

        self.__tela_atendimento.mostra_mensagem("Pagamento alterado com sucesso!")

    def retorna(self) -> None:
        pass

    def abre_tela(self) -> None:
        while True:
            try:
                opcao = self.__tela_atendimento.tela_opcoes()

                if opcao == 1:  # Agendar Atendimento
                    dados = self.__tela_atendimento.pega_dados_agendamento()
                    sistema = self.__controlador_sistema

                    erros = []

                    # 1. Valida Clínica
                    clinica = sistema.controlador_clinica.busca_clinica(dados["nome_clinica"])
                    if clinica is None:
                        erros.append(str(ClinicaNaoCadastradaException(dados["nome_clinica"])))

                    # 2. Valida Paciente
                    paciente = sistema.controlador_paciente.busca_paciente(dados["cpf_paciente"])
                    if paciente is None:
                        erros.append(str(PacienteNaoCadastradoException(dados["cpf_paciente"])))

                    # 3. Valida Profissional
                    profissional = sistema.controlador_profissional.busca_profissional(dados["cpf_profissional"])
                    if profissional is None:
                        erros.append(str(ProfissionalNaoCadastradoException(dados["cpf_profissional"])))

                    # 4. Valida Tipo de Atendimento
                    tipo = sistema.controlador_tipo_atendimento.busca_tipo_atendimento(dados["codigo_tipo"])
                    if tipo is None:
                        erros.append(str(TipoAtendimentoNaoCadastradoException(dados["codigo_tipo"])))

                    # Lança exceção acumulada de dados ausentes
                    if erros:
                        raise Exception("\n".join(erros))

                    acompanhante = None

                    if not paciente.maior_de_idade(dados["data"]):
                        self.__tela_atendimento.mostra_mensagem(
                            "Informe o acompanhante do paciente menor de idade."
                        )

                        acompanhante = Acompanhante(
                            **self.__tela_atendimento.pega_dados_acompanhante()
                        )

                        nascimento = acompanhante.data_nascimento
                        data_atendimento = dados["data"]

                        idade = data_atendimento.year - nascimento.year

                        if (data_atendimento.month, data_atendimento.day) < (nascimento.month, nascimento.day):
                            idade -= 1

                        if idade < 18:
                            raise AcompanhanteMenorDeIdadeException()

                    atendimento = Atendimento(
                        clinica, paciente, profissional, dados["data"],
                        dados["hora_inicio"], dados["hora_fim"], tipo,
                        dados["valor"], self.__proximo_numero, acompanhante
                    )
                    self.agenda_atendimento(atendimento)

                elif opcao == 2:  # Reagendar
                    num = self.__tela_atendimento.seleciona_atendimento()
                    dados = self.__tela_atendimento.pega_dados_reagendamento()
                    self.reagenda_atendimento(num, dados["hora_inicio"], dados["hora_fim"], dados["data"])

                elif opcao == 3:  # Cancelar
                    num = self.__tela_atendimento.seleciona_atendimento()
                    self.cancela_atendimento(num)

                elif opcao == 4:  # Incluir Procedimento
                    num = self.__tela_atendimento.seleciona_atendimento()
                    descricao = self.__tela_atendimento.seleciona_procedimento()
                    proc = self.__controlador_sistema.controlador_procedimento.busca_procedimento(descricao)
                    self.inclui_procedimento(num, proc)

                elif opcao == 5:  # Registrar Pagamento
                    num = self.__tela_atendimento.seleciona_atendimento()
                    atendimento = self.busca_atendimento(num)
                    if atendimento is None:
                        self.__tela_atendimento.mostra_mensagem("Atendimento não encontrado!")
                        continue

                    modalidade = self.__tela_atendimento.seleciona_forma_pagamento()
                    if modalidade == 1:
                        dados_p = self.__tela_atendimento.pega_dados_dinheiro()
                        pagamento = PagamentoDinheiro(dados_p["data"], atendimento, dados_p["valor_pagamento"])
                    elif modalidade == 2:
                        dados_p = self.__tela_atendimento.pega_dados_pix()
                        pagamento = PagamentoPix(dados_p["data"], atendimento, dados_p["valor_pagamento"], dados_p["cpf"])
                    elif modalidade == 3:
                        dados_p = self.__tela_atendimento.pega_dados_cartao()
                        pagamento = PagamentoCartao(
                            dados_p["data"], atendimento, dados_p["valor_pagamento"],
                            dados_p["bandeira"], dados_p["numero"], dados_p["parcelas"]
                        )
                    else:
                        continue

                    self.registra_pagamento(num, pagamento)

                elif opcao == 6:  # Listar Atendimentos
                    if not self.__atendimentos:
                        self.__tela_atendimento.mostra_mensagem("Nenhum atendimento cadastrado.")
                    else:
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

                elif opcao == 7:  # Listar Pagamentos
                    num = self.__tela_atendimento.seleciona_atendimento()
                    pagamentos = self.lista_pagamentos(num)
                    if pagamentos:
                        self.__tela_atendimento.mostra_pagamentos([p.mostra_dados() for p in pagamentos])
                    else:
                        self.__tela_atendimento.mostra_mensagem("Atendimento não encontrado ou sem pagamentos!")

                elif opcao == 8:  # Alterar Pagamento
                    num = self.__tela_atendimento.seleciona_atendimento()
                    atendimento = self.busca_atendimento(num)
                    if atendimento is None or not atendimento.pagamentos:
                        self.__tela_atendimento.mostra_mensagem("Atendimento sem pagamentos!")
                    else:
                        self.__tela_atendimento.mostra_pagamentos([p.mostra_dados() for p in atendimento.pagamentos])
                        indice = self.__tela_atendimento.seleciona_indice("Número do pagamento")
                        dados_p = self.__tela_atendimento.pega_dados_alteracao_pagamento()
                        self.altera_pagamento(num, indice, dados_p)

                elif opcao == 9:  # Excluir Pagamento
                    num = self.__tela_atendimento.seleciona_atendimento()
                    pagamentos = self.lista_pagamentos(num)
                    if not pagamentos:
                        self.__tela_atendimento.mostra_mensagem("Nenhum pagamento encontrado!")
                    else:
                        self.__tela_atendimento.mostra_pagamentos([p.mostra_dados() for p in pagamentos])
                        indice = self.__tela_atendimento.seleciona_indice("Número do pagamento")
                        self.exclui_pagamento(num, indice)

                elif opcao == 10:  # Listar Procedimentos
                    num = self.__tela_atendimento.seleciona_atendimento()
                    procedimentos = self.lista_procedimentos_atendimento(num)
                    if procedimentos:
                        self.__tela_atendimento.mostra_procedimentos([p.mostra_dados() for p in procedimentos])
                    else:
                        self.__tela_atendimento.mostra_mensagem("Atendimento não encontrado ou sem procedimentos!")

                elif opcao == 11:  # Excluir Procedimento
                    num = self.__tela_atendimento.seleciona_atendimento()
                    procedimentos = self.lista_procedimentos_atendimento(num)
                    if not procedimentos:
                        self.__tela_atendimento.mostra_mensagem("Atendimento sem procedimentos!")
                    else:
                        self.__tela_atendimento.mostra_procedimentos([p.mostra_dados() for p in procedimentos])
                        idx = self.__tela_atendimento.seleciona_indice("Número do procedimento")
                        if 0 <= idx < len(procedimentos):
                            self.exclui_procedimento_atendimento(num, procedimentos[idx])

                elif opcao == 12:  # Alterar Dados do Atendimento
                    num = self.__tela_atendimento.seleciona_atendimento()
                    if self.busca_atendimento(num) is None:
                        self.__tela_atendimento.mostra_mensagem("Atendimento não encontrado!")
                    else:
                        dados = self.__tela_atendimento.pega_dados_alteracao()
                        atualizacoes = {"valor": dados.get("valor")}

                        erros_alt = []
                        if dados.get("cpf_profissional"):
                            p = self.__controlador_sistema.controlador_profissional.busca_profissional(dados["cpf_profissional"])
                            if p is None:
                                erros_alt.append(str(ProfissionalNaoCadastradoException(dados["cpf_profissional"])))
                            else:
                                atualizacoes["profissional"] = p

                        if dados.get("codigo_tipo") is not None:
                            t = self.__controlador_sistema.controlador_tipo_atendimento.busca_tipo_atendimento(dados["codigo_tipo"])
                            if t is None:
                                erros_alt.append(str(TipoAtendimentoNaoCadastradoException(dados["codigo_tipo"])))
                            else:
                                atualizacoes["tipo_atendimento"] = t

                        if erros_alt:
                            raise Exception("\n".join(erros_alt))

                        self.altera_atendimento(num, atualizacoes)

                elif opcao == 0:
                    self.retorna()
                    break

            except Exception as erro:
                self.__tela_atendimento.mostra_mensagem(str(erro))