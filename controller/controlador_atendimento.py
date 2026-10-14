from datetime import date as Date, time as Time, datetime
from model.atendimento import Atendimento
from model.clinica import Clinica
from model.paciente import Paciente
from model.acompanhante import Acompanhante
from model.procedimento import Procedimento
from model.pagamento import Pagamento
from model.pagamentodinheiro import PagamentoDinheiro
from model.pagamentopix import PagamentoPix
from model.pagamentocartao import PagamentoCartao
from view.tela_atendimento import TelaAtendimento

class ControladorAtendimento:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_atendimento = TelaAtendimento()
        self.__atendimentos = []

    @property
    def atendimentos(self) -> list:
        return self.__atendimentos

    def valida_maioridade(self, paciente: Paciente, acomp: Acompanhante) -> bool:
        if paciente.maior_de_idade():
            return True
        return acomp is not None

    def valida_horario(self, clinica: Clinica, ini: Time, fim: Time) -> bool:
        return (
            clinica.esta_aberta_clinica(ini)
            and clinica.esta_aberta_clinica(fim)
            and ini < fim
        )

    def agenda_atendimento(self, atendimento: Atendimento) -> None:
        if not isinstance(atendimento, Atendimento):
            return

        if self.busca_atendimento(atendimento.numero_atendimento) is not None:
            self.__tela_atendimento.mostra_mensagem(
                "Já existe um atendimento com este número!"
            )
            return

        if not self.valida_maioridade(atendimento.paciente, atendimento.acompanhante):
            self.__tela_atendimento.mostra_mensagem(
                "Regra 1: Pacientes menores de 18 anos precisam de acompanhante!"
            )
            return

        if not self.valida_horario(
            atendimento.clinica, atendimento.hora_inicio, atendimento.hora_fim
        ):
            self.__tela_atendimento.mostra_mensagem(
                "Regra 2: O atendimento deve ocorrer dentro do horário de funcionamento da clínica!"
            )
            return

        self.__atendimentos.append(atendimento)
        atendimento.clinica.registra_atendimento(atendimento)
        self.__tela_atendimento.mostra_mensagem("Atendimento agendado com sucesso!")

    def cancela_atendimento(self, numero_atendimento: int) -> None:
        atendimento = self.busca_atendimento(numero_atendimento)
        if atendimento is not None:
            self.__atendimentos.remove(atendimento)
            atendimento.clinica.cancela_atendimento(atendimento)
            self.__tela_atendimento.mostra_mensagem(
                "Atendimento cancelado com sucesso!"
            )
        else:
            self.__tela_atendimento.mostra_mensagem("Atendimento não encontrado!")

    def reagenda_atendimento(
        self, numero_atendimento: int, hora_inicio: Time, hora_fim: Time, data: Date
    ) -> None:
        atendimento = self.busca_atendimento(numero_atendimento)
        if atendimento is None:
            self.__tela_atendimento.mostra_mensagem("Atendimento não encontrado!")
            return

        if not self.valida_horario(atendimento.clinica, hora_inicio, hora_fim):
            self.__tela_atendimento.mostra_mensagem(
                "Regra 2: O novo horário está fora do funcionamento da clínica!"
            )
            return

        atendimento.data = data
        atendimento.hora_inicio = hora_inicio
        atendimento.hora_fim = hora_fim
        self.__tela_atendimento.mostra_mensagem("Atendimento reagendado com sucesso!")

    def busca_atendimento(self, numero_atendimento: int) -> Atendimento:
        for atendimento in self.__atendimentos:
            if atendimento.numero_atendimento == numero_atendimento:
                return atendimento
        return None

    def inclui_procedimento(
        self, numero_atendimento: int, procedimento: Procedimento
    ) -> None:
        atendimento = self.busca_atendimento(numero_atendimento)
        if atendimento is not None and isinstance(procedimento, Procedimento):
            atendimento.inclui_procedimento(procedimento)
            self.__tela_atendimento.mostra_mensagem(
                "Procedimento incluído no atendimento com sucesso!"
            )
        else:
            self.__tela_atendimento.mostra_mensagem(
                "Erro ao incluir procedimento: Atendimento ou Procedimento inválido!"
            )

    def registra_pagamento(
        self, numero_atendimento: int, pagamento: Pagamento
    ) -> None:
        atendimento = self.busca_atendimento(numero_atendimento)
        if atendimento is None:
            self.__tela_atendimento.mostra_mensagem("Atendimento não encontrado!")
            return

        if pagamento.data > atendimento.data:
            self.__tela_atendimento.mostra_mensagem(
                "Regra 3: O pagamento deve ser realizado até a data do atendimento!"
            )
            return

        if pagamento.valor_pagamento <= 0:
            self.__tela_atendimento.mostra_mensagem(
                "O valor do pagamento deve ser maior que zero!"
            )
            return

        if pagamento.valor_pagamento > atendimento.mostra_valor_restante():
            self.__tela_atendimento.mostra_mensagem(
                f"Valor excede o restante a pagar (R$ {atendimento.mostra_valor_restante():.2f})!"
            )
            return

        atendimento.adiciona_pagamento(pagamento)
        self.__tela_atendimento.mostra_mensagem(
            f"Pagamento registrado! Valor restante: R$ {atendimento.mostra_valor_restante():.2f}"
        )

    def retorna(self) -> None:
        pass

    def abre_tela(self) -> None:
        lista_opcoes = {
            1: self.__agendar,
            2: self.__reagendar,
            3: self.__cancelar,
            4: self.__incluir_proc,
            5: self.__pagar,
            6: self.__listar,
            0: self.retorna,
        }

        while True:
            opcao_escolhida = self.__tela_atendimento.tela_opcoes()
            funcao_escolhida = lista_opcoes.get(opcao_escolhida)

            if funcao_escolhida:
                funcao_escolhida()
                if opcao_escolhida == 0:
                    break
            else:
                self.__tela_atendimento.mostra_mensagem(
                    "Opção inválida! Escolha um número do menu."
                )

    def __agendar(self) -> None:
        dados = self.__tela_atendimento.pega_dados_agendamento()

        clinica = self.__controlador_sistema.controlador_clinica.busca_clinica(
            dados["nome_clinica"]
        )
        if clinica is None:
            self.__tela_atendimento.mostra_mensagem("Clínica não encontrada!")
            return

        paciente = self.__controlador_sistema.controlador_paciente.busca_paciente(
            dados["cpf_paciente"]
        )
        if paciente is None:
            self.__tela_atendimento.mostra_mensagem("Paciente não encontrado!")
            return

        profissional = (
            self.__controlador_sistema.controlador_profissional.busca_profissional(
                dados["cpf_profissional"]
            )
        )
        if profissional is None:
            self.__tela_atendimento.mostra_mensagem("Profissional não encontrado!")
            return

        tipo = self.__controlador_sistema.controlador_tipo_atendimento.busca_tipo_atendimento(
            dados["codigo_tipo"]
        )
        if tipo is None:
            self.__tela_atendimento.mostra_mensagem(
                "Tipo de atendimento não encontrado!"
            )
            return

        acompanhante = None
        if not paciente.maior_de_idade():
            self.__tela_atendimento.mostra_mensagem(
                "Paciente menor de 18 anos! Informe os dados do acompanhante:"
            )
            dados_acomp = self.__tela_atendimento.pega_dados_acompanhante()
            acompanhante = Acompanhante(
                cpf=dados_acomp["cpf"],
                nome=dados_acomp["nome"],
                celular=dados_acomp["celular"],
                data_nascimento=dados_acomp["data_nascimento"],
                relacao_paciente=dados_acomp["relacao_paciente"],
            )

        novo_atendimento = Atendimento(
            clinica=clinica,
            paciente=paciente,
            profissional=profissional,
            data=dados["data"],
            hora_inicio=dados["hora_inicio"],
            hora_fim=dados["hora_fim"],
            tipo_atendimento=tipo,
            valor=dados["valor"],
            numero_atendimento=dados["numero_atendimento"],
            acompanhante=acompanhante,
        )
        self.agenda_atendimento(novo_atendimento)

    def __reagendar(self) -> None:
        self.__listar()
        if not self.__atendimentos:
            return
        num = self.__tela_atendimento.seleciona_atendimento()
        try:
            data_str = input("Nova Data (DD/MM/AAAA): ").strip()
            nova_data = datetime.strptime(data_str, "%d/%m/%Y").date()
            ini_str = input("Novo Horário de Início (HH:MM): ").strip()
            novo_ini = datetime.strptime(ini_str, "%H:%M").time()
            fim_str = input("Novo Horário de Fim (HH:MM): ").strip()
            novo_fim = datetime.strptime(fim_str, "%H:%M").time()
            self.reagenda_atendimento(num, novo_ini, novo_fim, nova_data)
        except ValueError:
            self.__tela_atendimento.mostra_mensagem("Formato de data ou hora inválido!")

    def __cancelar(self) -> None:
        self.__listar()
        if not self.__atendimentos:
            return
        num = self.__tela_atendimento.seleciona_atendimento()
        self.cancela_atendimento(num)

    def __incluir_proc(self) -> None:
        self.__listar()
        if not self.__atendimentos:
            return
        num = self.__tela_atendimento.seleciona_atendimento()
        descricao = input("Descrição do procedimento: ").strip()
        proc = self.__controlador_sistema.controlador_procedimento.busca_procedimento(
            descricao
        )
        if proc is None:
            self.__tela_atendimento.mostra_mensagem("Procedimento não encontrado!")
            return
        self.inclui_procedimento(num, proc)

    def __pagar(self) -> None:
        self.__listar()
        if not self.__atendimentos:
            return
        num = self.__tela_atendimento.seleciona_atendimento()
        atendimento = self.busca_atendimento(num)
        if atendimento is None:
            self.__tela_atendimento.mostra_mensagem("Atendimento não encontrado!")
            return

        modalidade = self.__tela_atendimento.seleciona_forma_pagamento()
        if modalidade == 1:
            d = self.__tela_atendimento.pega_dados_dinheiro()
            pag = PagamentoDinheiro(d["data"], atendimento, d["valor_pagamento"])
        elif modalidade == 2:
            d = self.__tela_atendimento.pega_dados_pix()
            pag = PagamentoPix(d["data"], atendimento, d["valor_pagamento"], d["cpf"])
        elif modalidade == 3:
            d = self.__tela_atendimento.pega_dados_cartao()
            pag = PagamentoCartao(
                d["data"],
                atendimento,
                d["valor_pagamento"],
                d["bandeira"],
                d["numero"],
                d["parcelas"],
            )
        else:
            self.__tela_atendimento.mostra_mensagem("Modalidade inválida!")
            return

        self.registra_pagamento(num, pag)

    def __listar(self) -> None:
        if not self.__atendimentos:
            self.__tela_atendimento.mostra_mensagem("Nenhum atendimento cadastrado.")
            return
        print("\n--- LISTA DE ATENDIMENTOS ---")
        for a in self.__atendimentos:
            self.__tela_atendimento.mostra_atendimento(
                {
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
                    "pago": "Sim" if a.pago() else "Não",
                }
            )