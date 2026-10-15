from view.tela_relatorio import TelaRelatorio


class ControladorRelatorio:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_relatorio = TelaRelatorio()

    def relatorio_clinicas_mais_atendimentos(self) -> None:
        clinicas = self.__controlador_sistema.controlador_clinica.clinicas
        if not clinicas:
            self.__tela_relatorio.mostra_mensagem("Nenhuma clínica cadastrada.")
            return

        clinicas_ordenadas = sorted(
            clinicas, key=lambda c: len(c.atendimentos), reverse=True
        )

        dados = []
        for pos, clinica in enumerate(clinicas_ordenadas, start=1):
            dados.append(
                f"{pos}º - Clínica: {clinica.nome} ({clinica.cidade}) | "
                f"Total de Atendimentos: {len(clinica.atendimentos)}"
            )

        self.__tela_relatorio.mostra_relatorio(
            "CLÍNICAS COM MAIS ATENDIMENTOS", dados
        )

    def relatorio_atendimentos_caros_baratos(self) -> None:
        atendimentos = self.__controlador_sistema.controlador_atendimento.atendimentos
        if not atendimentos:
            self.__tela_relatorio.mostra_mensagem("Nenhum atendimento registrado.")
            return

        mais_caro = max(atendimentos, key=lambda a: a.valor_total)
        mais_barato = min(atendimentos, key=lambda a: a.valor_total)

        dados = [
            f"Mais Caro   -> Atendimento Nº {mais_caro.numero_atendimento} | "
            f"Paciente: {mais_caro.paciente.nome} | Clínica: {mais_caro.clinica.nome} | "
            f"Valor Total: R$ {mais_caro.valor_total:.2f}",
            f"Mais Barato -> Atendimento Nº {mais_barato.numero_atendimento} | "
            f"Paciente: {mais_barato.paciente.nome} | Clínica: {mais_barato.clinica.nome} | "
            f"Valor Total: R$ {mais_barato.valor_total:.2f}",
        ]

        self.__tela_relatorio.mostra_relatorio(
            "ATENDIMENTOS MAIS CAROS E MAIS BARATOS", dados
        )

    def relatorio_procedimentos_populares(self) -> None:
        atendimentos = self.__controlador_sistema.controlador_atendimento.atendimentos
        contagem = {}

        for atendimento in atendimentos:
            for proc in atendimento.procedimentos:
                contagem[proc.descricao] = contagem.get(proc.descricao, 0) + 1

        if not contagem:
            self.__tela_relatorio.mostra_mensagem(
                "Nenhum procedimento foi realizado em atendimentos ainda."
            )
            return

        populares = sorted(contagem.items(), key=lambda item: item[1], reverse=True)

        dados = []
        for pos, (descricao, qtd) in enumerate(populares, start=1):
            dados.append(f"{pos}º - Procedimento: {descricao} | Realizado: {qtd} vez(es)")

        self.__tela_relatorio.mostra_relatorio(
            "PROCEDIMENTOS MAIS REALIZADOS (POPULARES)", dados
        )

    def relatorio_procedimentos_caros_baratos(self) -> None:
        procedimentos = (
            self.__controlador_sistema.controlador_procedimento.procedimentos
        )
        if not procedimentos:
            self.__tela_relatorio.mostra_mensagem("Nenhum procedimento cadastrado.")
            return

        mais_caro = max(procedimentos, key=lambda p: p.custo)
        mais_barato = min(procedimentos, key=lambda p: p.custo)

        dados = [
            f"Mais Caro   -> {mais_caro.descricao} | Profissional: {mais_caro.profissional.nome} | "
            f"Custo: R$ {mais_caro.custo:.2f}",
            f"Mais Barato -> {mais_barato.descricao} | Profissional: {mais_barato.profissional.nome} | "
            f"Custo: R$ {mais_barato.custo:.2f}",
        ]

        self.__tela_relatorio.mostra_relatorio(
            "PROCEDIMENTOS MAIS CAROS E MAIS BARATOS", dados
        )

    def retorna(self) -> None:
        pass

    def abre_tela(self) -> None:
        while True:
            try:
                opcao = self.__tela_relatorio.tela_opcoes()

                if opcao == 1:
                    self.relatorio_clinicas_mais_atendimentos()
                elif opcao == 2:
                    self.relatorio_atendimentos_caros_baratos()
                elif opcao == 3:
                    self.relatorio_procedimentos_populares()
                elif opcao == 4:
                    self.relatorio_procedimentos_caros_baratos()
                elif opcao == 0:
                    self.retorna()
                    break
                else:
                    self.__tela_relatorio.mostra_mensagem(
                        "Opção inválida! Escolha um número do menu."
                    )
            except Exception as erro:
                self.__tela_relatorio.mostra_mensagem(str(erro))