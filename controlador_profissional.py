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

    def abre_tela(self) -> None:
        lista_opcoes = {
            1: self.__incluir,
            2: self.__excluir,
            3: self.__alterar_nome,
            4: self.__alterar_cpf,
            5: self.__alterar_registro,
            6: self.__alterar_especialidade,
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

    def __excluir(self) -> None:
        cpf = self.__tela_profissional.seleciona_profissional()
        self.exclui_profissional(cpf)

    def __alterar_nome(self) -> None:
        cpf = self.__tela_profissional.seleciona_profissional()
        dados = self.__tela_profissional.pega_dados_profissional()
        self.altera_nome(cpf, dados["nome"])

    def __alterar_cpf(self) -> None:
        cpf_atual = self.__tela_profissional.seleciona_profissional()
        dados = self.__tela_profissional.pega_dados_profissional()
        self.altera_cpf(cpf_atual, dados["cpf"])

    def __alterar_registro(self) -> None:
        registro_atual = self.__tela_profissional.seleciona_profissional()
        dados = self.__tela_profissional.pega_dados_profissional()
        self.altera_registro(registro_atual, dados["registro_profissional"])

    def __alterar_especialidade(self) -> None:
        registro = self.__tela_profissional.seleciona_profissional()
        dados = self.__tela_profissional.pega_dados_profissional()
        self.altera_especialidade(registro, dados["especialidade"])