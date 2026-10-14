from model.profissional import Profissional
from view.tela_profissional import TelaProfissional


class ControladorProfissional:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_profissional = TelaProfissional()
        self.__profissionais = []

    @property
    def profissionais(self):
        return self.__profissionais

    def cadastra_profissional(self, profissional: Profissional):
        if isinstance(profissional, Profissional):
            if self.busca_profissional(profissional.cpf) is None:
                self.__profissionais.append(profissional)
                self.__tela_profissional.mostra_mensagem("Profissional cadastrado com sucesso!")
            else:
                self.__tela_profissional.mostra_mensagem("Erro: Já existe um profissional com este CPF")

    def exclui_profissional(self, cpf: str):
        profissional = self.busca_profissional(cpf)
        if profissional is not None:
            self.__profissionais.remove(profissional)
            self.__tela_profissional.mostra_mensagem("Profissional excluído com sucesso")
        else:
            self.__tela_profissional.mostra_mensagem("Erro: Profissional não encontrado")

    def altera_especialidade(self, registro: str, nova_especialidade: str):
        for profissional in self.__profissionais:
            if profissional.registro_profissional == registro:
                profissional.especialidade = nova_especialidade
                self.__tela_profissional.mostra_mensagem("Especialidade alterada com sucesso")
                return
        self.__tela_profissional.mostra_mensagem("Erro: Profissional não encontrado pelo registro")

    def altera_registro(self, registro_atual: str, novo_registro: str):
        for profissional in self.__profissionais:
            if profissional.registro_profissional == registro_atual:
                profissional.registro_profissional = novo_registro
                self.__tela_profissional.mostra_mensagem("Registro profissional alterado com sucesso!")
                return
        self.__tela_profissional.mostra_mensagem("Erro: Profissional não encontrado pelo registro atual!")

    def altera_nome(self, cpf: str, novo_nome: str):
        profissional = self.busca_profissional(cpf)
        if profissional is not None:
            profissional.nome = novo_nome
            self.__tela_profissional.mostra_mensagem("Nome alterado com sucesso!")
        else:
            self.__tela_profissional.mostra_mensagem("Erro: Profissional não encontrado!")

    def altera_cpf(self, cpf_atual: str, novo_cpf: str):
        profissional = self.busca_profissional(cpf_atual)
        if profissional is not None:
            if self.busca_profissional(novo_cpf) is None:
                profissional.cpf = novo_cpf
                self.__tela_profissional.mostra_mensagem("CPF alterado com sucesso!")
            else:
                self.__tela_profissional.mostra_mensagem("Erro: Novo CPF já cadastrado para outro profissional!")
        else:
            self.__tela_profissional.mostra_mensagem("Erro: Profissional não encontrado!")

    def busca_profissional(self, cpf: str):
        for profissional in self.__profissionais:
            if profissional.cpf == cpf:
                return profissional
        return None

    def retorna(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            1: self.__incluir,
            2: self.__alterar,
            3: self.__listar,
            4: self.__excluir,
            0: self.retorna,
        }

        while True:
            opcao = self.__tela_profissional.mostra_opcoes()
            funcao_escolhida = lista_opcoes.get(opcao)
            if funcao_escolhida:
                funcao_escolhida()
            if opcao == 0:
                break

    def __incluir(self):
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

    def __alterar(self):
        self.__listar()
        if not self.__profissionais:
            return
        
        opcao_alterar = self.__tela_profissional.mostra_opcoes_alteracao()
        if opcao_alterar == 1:
            cpf = self.__tela_profissional.seleciona_cpf()
            novo_nome = self.__tela_profissional.pega_novo_nome()
            self.altera_nome(cpf, novo_nome)
        elif opcao_alterar == 2:
            cpf_atual = self.__tela_profissional.seleciona_cpf()
            novo_cpf = self.__tela_profissional.pega_novo_cpf()
            self.altera_cpf(cpf_atual, novo_cpf)
        elif opcao_alterar == 3:
            registro_atual = self.__tela_profissional.seleciona_registro()
            novo_registro = self.__tela_profissional.pega_novo_registro()
            self.altera_registro(registro_atual, novo_registro)
        elif opcao_alterar == 4:
            registro = self.__tela_profissional.seleciona_registro()
            nova_esp = self.__tela_profissional.pega_nova_especialidade()
            self.altera_especialidade(registro, nova_esp)

    def __listar(self):
        if not self.__profissionais:
            self.__tela_profissional.mostra_mensagem("Nenhum profissional cadastrado.")
            return
        self.__tela_profissional.mostra_mensagem("--- LISTA DE PROFISSIONAIS ---")
        for p in self.__profissionais:
            self.__tela_profissional.mostra_profissional(p.mostra_dados())

    def __excluir(self):
        self.__listar()
        if not self.__profissionais:
            return
        cpf = self.__tela_profissional.seleciona_cpf()
        self.exclui_profissional(cpf)