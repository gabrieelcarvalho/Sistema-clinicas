from datetime import time
from model.clinica import Clinica
from view.tela_clinica import TelaClinica
from exceptions.clinica_nao_cadastrada_exception import ClinicaNaoCadastradaException


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

    def cadastra_clinica(self, clinica: Clinica) -> None:
        if (
            not isinstance(clinica, Clinica)
            or not clinica.nome.strip()
            or not clinica.cidade.strip()
        ):
            self.__tela_clinica.mostra_mensagem("Nome e cidade são obrigatórios!")
        elif self.busca_clinica(clinica.nome):
            self.__tela_clinica.mostra_mensagem("Já existe uma clínica com esse nome!")
        elif clinica.horario_abertura >= clinica.horario_fechamento:
            self.__tela_clinica.mostra_mensagem("Expediente inválido!")
        else:
            self.__clinicas.append(clinica)
            self.__tela_clinica.mostra_mensagem("Clínica cadastrada com sucesso!")

    def exclui_clinica(self, nome: str) -> None:
        clinica = self.busca_clinica(nome)
        if clinica is None:
            raise ClinicaNaoCadastradaException(nome)
        elif clinica.atendimentos:
            self.__tela_clinica.mostra_mensagem(
                "Cancele os atendimentos da clínica antes da exclusão!"
            )
        else:
            self.__clinicas.remove(clinica)
            self.__tela_clinica.mostra_mensagem("Clínica excluída com sucesso!")

    def altera_horario(self, clinica: Clinica, abertura: time, fechamento: time) -> None:
        if clinica not in self.__clinicas or abertura >= fechamento:
            self.__tela_clinica.mostra_mensagem("Clínica ou expediente inválido!")
        elif any(
            not (abertura <= a.hora_inicio < a.hora_fim <= fechamento)
            for a in clinica.atendimentos
        ):
            self.__tela_clinica.mostra_mensagem(
                "O novo horário excluiria atendimentos já marcados!"
            )
        else:
            clinica.horario_abertura = abertura
            clinica.horario_fechamento = fechamento
            self.__tela_clinica.mostra_mensagem("Horário alterado com sucesso!")

    def clinicas_abertas(self, hora: time) -> list:
        return [c for c in self.__clinicas if c.esta_aberta_clinica(hora)]

    def altera_nome(self, nome_atual: str, novo_nome: str):
        clinica = self.busca_clinica(nome_atual)
        if clinica is None:
            raise ClinicaNaoCadastradaException(nome_atual)
        if not novo_nome.strip():
            self.__tela_clinica.mostra_mensagem("Nome inválido!")
        elif self.busca_clinica(novo_nome) not in (None, clinica):
            self.__tela_clinica.mostra_mensagem("Nome já utilizado!")
        else:
            clinica.nome = novo_nome
            self.__tela_clinica.mostra_mensagem("Nome alterado!")

    def altera_cidade(self, nome: str, nova_cidade: str):
        clinica = self.busca_clinica(nome)
        if clinica is None:
            raise ClinicaNaoCadastradaException(nome)
        if not nova_cidade.strip():
            self.__tela_clinica.mostra_mensagem("Cidade vazia!")
            return
        clinica.cidade = nova_cidade
        self.__tela_clinica.mostra_mensagem("Dado alterado com sucesso!")

    def altera_descricao(self, nome: str, nova_descricao: str):
        clinica = self.busca_clinica(nome)
        if clinica is None:
            raise ClinicaNaoCadastradaException(nome)
        if not nova_descricao.strip():
            self.__tela_clinica.mostra_mensagem("Descrição vazia!")
            return
        clinica.descricao = nova_descricao
        self.__tela_clinica.mostra_mensagem("Dado alterado com sucesso!")

    def retorna(self):
        pass

    def abre_tela(self):
        while True:
            try:
                opcao = self.__tela_clinica.tela_opcoes()

                if opcao == 1:  # Cadastrar
                    dados = self.__tela_clinica.pega_dados_clinica()
                    self.cadastra_clinica(
                        Clinica(
                            dados["nome"],
                            dados["cidade"],
                            dados["descricao"],
                            dados["abertura"],
                            dados["fechamento"]
                        )
                    )

                elif opcao == 2:  # Excluir
                    nome = self.__tela_clinica.seleciona_clinica()
                    self.exclui_clinica(nome)

                elif opcao == 3:  # Alterar Horários
                    nome = self.__tela_clinica.seleciona_clinica()
                    clinica = self.busca_clinica(nome)
                    if clinica is None:
                        raise ClinicaNaoCadastradaException(nome)
                    dados = self.__tela_clinica.pega_novos_horarios()
                    self.altera_horario(clinica, dados["abertura"], dados["fechamento"])

                elif opcao == 4:  # Listar Abertas
                    hora = self.__tela_clinica.pega_horario("Horário de consulta")
                    abertas = self.clinicas_abertas(hora)
                    if not abertas:
                        self.__tela_clinica.mostra_mensagem("Nenhuma clínica encontrada!")
                    else:
                        for c in abertas:
                            self.__tela_clinica.mostra_clinica({
                                "nome": c.nome,
                                "cidade": c.cidade,
                                "descricao": c.descricao,
                                "abertura": c.horario_abertura,
                                "fechamento": c.horario_fechamento
                            })

                elif opcao == 5:  # Listar Todas
                    if not self.__clinicas:
                        self.__tela_clinica.mostra_mensagem("Nenhuma clínica encontrada!")
                    else:
                        for c in self.__clinicas:
                            self.__tela_clinica.mostra_clinica({
                                "nome": c.nome,
                                "cidade": c.cidade,
                                "descricao": c.descricao,
                                "abertura": c.horario_abertura,
                                "fechamento": c.horario_fechamento
                            })

                elif opcao == 6:  # Editar Nome
                    nome = self.__tela_clinica.seleciona_clinica()
                    valor = self.__tela_clinica.pega_novo_dado("nome")
                    self.altera_nome(nome, valor)

                elif opcao == 7:  # Editar Cidade
                    nome = self.__tela_clinica.seleciona_clinica()
                    valor = self.__tela_clinica.pega_novo_dado("cidade")
                    self.altera_cidade(nome, valor)

                elif opcao == 8:  # Editar Descrição
                    nome = self.__tela_clinica.seleciona_clinica()
                    valor = self.__tela_clinica.pega_novo_dado("descricao")
                    self.altera_descricao(nome, valor)

                elif opcao == 0:
                    self.retorna()
                    break

            except Exception as erro:
                self.__tela_clinica.mostra_mensagem(str(erro))