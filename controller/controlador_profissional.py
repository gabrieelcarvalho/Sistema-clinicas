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

    # --- Métodos de Negócio / CRUD ---

    def cadastra_profissional(self, profissional: Profissional) -> None:
        if isinstance(profissional, Profissional):
            if self.busca_profissional(profissional.cpf) is None:
                self.__profissionais.append(profissional)
                self.__tela_profissional.mostra_mensagem("Profissional cadastrado com sucesso!")
            else:
                self.__tela_profissional.mostra_mensagem("Erro: Já existe um profissional com este CPF!")

    def exclui_profissional(self, cpf: str) -> None:
        profissional = self.busca_profissional(cpf)
        if profissional is not None:
            self.__profissionais.remove(profissional)
            self.__tela_profissional.mostra_mensagem("Profissional excluído com sucesso!")
        else:
            self.__tela_profissional.mostra_mensagem("Erro: Profissional não encontrado!")

    def altera_especialidade(self, registro: str, nova_especialidade: str) -> None:
        for profissional in self.__profissionais:
            if profissional.registro_profissional == registro:
                profissional.especialidade = nova_especialidade
                self.__tela_profissional.mostra_mensagem("Especialidade alterada com sucesso!")
                return
        self.__tela_profissional.mostra_mensagem("Erro: Profissional não encontrado pelo registro!")

    def altera_registro(self, registro_atual: str, novo_registro: str) -> None:
        for profissional in self.__profissionais:
            if profissional.registro_profissional == registro_atual:
                profissional.registro_profissional = novo_registro
                self.__tela_profissional.mostra_mensagem("Registro profissional alterado com sucesso!")
                return
        self.__tela_profissional.mostra_mensagem("Erro: Profissional não encontrado pelo registro atual!")

    def altera_nome(self, cpf: str, novo_nome: str) -> None:
        profissional = self.busca_profissional(cpf)
        if profissional is not None:
            profissional.nome = novo_nome
            self.__tela_profissional.mostra_mensagem("Nome alterado com sucesso!")
        else:
            self.__tela_profissional.mostra_mensagem("Erro: Profissional não encontrado!")

    def altera_cpf(self, cpf_atual: str, novo_cpf: str) -> None:
        profissional = self.busca_profissional(cpf_atual)
        if profissional is not None:
            if self.busca_profissional(novo_cpf) is None:
                profissional.cpf = novo_cpf
                self.__tela_profissional.mostra_mensagem("CPF alterado com sucesso!")
            else:
                self.__tela_profissional.mostra_mensagem("Erro: Novo CPF já cadastrado para outro profissional!")
        else:
            self.__tela_profissional.mostra_mensagem("Erro: Profissional não encontrado!")

    def busca_profissional(self, cpf: str) -> Profissional | None:
        for profissional in self.__profissionais:
            if profissional.cpf == cpf:
                return profissional
        return None

    def retorna(self) -> None:
        pass

    # --- Navegação do Submenu ---

    def abre_tela(self) -> None:
        lista_opcoes = {
            1: self.__incluir,
            2: self.__alterar,
            3: self.__listar,
            4: self.__excluir,
            0: self.retorna,
        }

        while True:
            opcao_escolhida = self.__tela_profissional.tela_opcoes()
            funcao_escolhida = lista_opcoes.get(opcao_escolhida)

            if funcao_escolhida:
                funcao_escolhida()
            else:
                self.__tela_profissional.mostra_mensagem("Opção inválida! Escolha um número do menu.")

            if opcao_escolhida == 0:
                break

    # --- Métodos Auxiliares Privados ---

    def __incluir(self) -> None:
        dados = self.__tela_profissional.pega_dados_profissional()
        if dados:
            novo = Profissional(
                cpf=dados["cpf"],
                nome=dados["nome"],
                celular=dados["celular"],
                especialidade=dados["especialidade"],
                registro_profissional=dados["registro_profissional"],
            )
            self.cadastra_profissional(novo)

    def __alterar(self) -> None:
        if not self.__profissionais:
            self.__tela_profissional.mostra_mensagem("Nenhum profissional cadastrado para alterar.")
            return

        self.__listar()

        lista_opcoes_alteracao = {
            1: self.__alterar_nome_aux,
            2: self.__alterar_cpf_aux,
            3: self.__alterar_registro_aux,
            4: self.__alterar_especialidade_aux,
            0: self.retorna,
        }

        opcao_escolhida = self.__tela_profissional.tela_opcoes_alteracao()
        funcao_escolhida = lista_opcoes_alteracao.get(opcao_escolhida)

        if funcao_escolhida:
            funcao_escolhida()
        else:
            self.__tela_profissional.mostra_mensagem("Opção inválida ou operação cancelada.")

    def __alterar_nome_aux(self) -> None:
        cpf = self.__tela_profissional.seleciona_cpf()
        novo_nome = self.__tela_profissional.pega_novo_nome()
        self.altera_nome(cpf, novo_nome)

    def __alterar_cpf_aux(self) -> None:
        cpf_atual = self.__tela_profissional.seleciona_cpf()
        novo_cpf = self.__tela_profissional.pega_novo_cpf()
        self.altera_cpf(cpf_atual, novo_cpf)

    def __alterar_registro_aux(self) -> None:
        registro_atual = self.__tela_profissional.seleciona_registro()
        novo_registro = self.__tela_profissional.pega_novo_registro()
        self.altera_registro(registro_atual, novo_registro)

    def __alterar_especialidade_aux(self) -> None:
        registro = self.__tela_profissional.seleciona_registro()
        nova_esp = self.__tela_profissional.pega_nova_especialidade()
        self.altera_especialidade(registro, nova_esp)

    def __listar(self) -> None:
        if not self.__profissionais:
            self.__tela_profissional.mostra_mensagem("Nenhum profissional cadastrado.")
            return
        self.__tela_profissional.mostra_mensagem("--- LISTA DE PROFISSIONAIS ---")
        for p in self.__profissionais:
            self.__tela_profissional.mostra_profissional(p.mostra_dados())

    def __excluir(self) -> None:
        if not self.__profissionais:
            self.__tela_profissional.mostra_mensagem("Nenhum profissional cadastrado para excluir.")
            return
        self.__listar()
        cpf = self.__tela_profissional.seleciona_cpf()
        self.exclui_profissional(cpf)