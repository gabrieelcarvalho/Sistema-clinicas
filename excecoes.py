"""Exceções de negócio do sistema de gerenciamento de clínicas.

Este módulo apenas DEFINE os tipos de erro. As validações que os disparam
ficam no Model ou nos controladores; a interface mostra as mensagens ao usuário.
"""


class ErroSistemaClinicas(Exception):
    """Classe-base para os erros previstos pelo sistema."""

    mensagem_padrao = "Ocorreu um erro no sistema de clínicas."

    def __init__(self, mensagem=None):
        super().__init__(mensagem if mensagem is not None else self.mensagem_padrao)


# Cadastros e busca
class DadosInvalidosError(ErroSistemaClinicas):
    """Dados obrigatórios ausentes, formato inválido ou valor inadequado."""

    mensagem_padrao = "Os dados informados são inválidos."

class CadastroDuplicadoError(ErroSistemaClinicas):
    """Tentativa de cadastrar um registro com identificador já existente."""

    mensagem_padrao = "Já existe um cadastro com esse identificador."


class RegistroNaoEncontradoError(ErroSistemaClinicas):
    """Tentativa de acessar, alterar ou excluir um registro inexistente."""

    mensagem_padrao = "Registro não encontrado."


# Agendamento e atendimento
class PacienteMenorDesacompanhadoError(ErroSistemaClinicas):
    """Paciente menor de idade sem acompanhante no atendimento."""

    mensagem_padrao = "Paciente menor de 18 anos precisa de acompanhante."


class HorarioInvalidoError(ErroSistemaClinicas):
    """Horário de início/fim incoerente ou expediente inválido."""

    mensagem_padrao = "O horário final deve ser posterior ao inicial."

class AtendimentoForaDoHorarioError(ErroSistemaClinicas):
    """Consulta marcada fora do funcionamento da clínica."""

    mensagem_padrao = "O atendimento deve ocorrer dentro do horário da clínica."


class ConflitoDeHorarioError(ErroSistemaClinicas):
    """Atendimento simultâneo conflitante para um profissional."""

    mensagem_padrao = "O profissional já possui atendimento nesse horário."

# Pagamentos
class PagamentoForaDoPrazoError(ErroSistemaClinicas):
    """Pagamento posterior à data do atendimento."""

    mensagem_padrao = "O pagamento deve ocorrer até a data do atendimento."


class ValorPagamentoInvalidoError(ErroSistemaClinicas):
    """Valor do pagamento menor ou igual a zero."""

    mensagem_padrao = "O valor do pagamento deve ser maior que zero."

class PagamentoExcedenteError(ErroSistemaClinicas):
    """Pagamento maior que o saldo restante do atendimento."""

    mensagem_padrao = "O pagamento excede o valor restante do atendimento."


class PagamentoDeOutroAtendimentoError(ErroSistemaClinicas):
    """Pagamento associado a um atendimento diferente do selecionado."""

    mensagem_padrao = "O pagamento não pertence a este atendimento."


class ModalidadePagamentoInvalidaError(ErroSistemaClinicas):
    """Modalidade diferente de dinheiro, PIX ou cartão de crédito."""

    mensagem_padrao = "Modalidade de pagamento inválida."