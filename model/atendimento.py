
from datetime import date as Date, time as Time
from model.clinica import Clinica
from model.paciente import Paciente
from model.profissional import Profissional
from model.acompanhante import Acompanhante
from model.tipoatendimento import TipoAtendimento
from model.procedimento import Procedimento


class Atendimento:
    def __init__(
        self, clinica: Clinica, paciente: Paciente,
        profissional: Profissional, data: Date,
        hora_inicio: Time, hora_fim: Time,
        tipo_atendimento: TipoAtendimento,
        valor: float, numero_atendimento: int,
        acompanhante: Acompanhante = None
    ):
        self.__clinica = clinica
        self.__paciente = paciente
        self.__profissional = profissional
        self.__data = data
        self.__hora_inicio = hora_inicio
        self.__hora_fim = hora_fim
        self.__tipo_atendimento = tipo_atendimento
        self.__valor = valor
        self.__numero_atendimento = numero_atendimento
        self.__acompanhante = acompanhante
        self.__pagamentos = []
        self.__procedimentos = []

    @property
    def clinica(self) -> Clinica:
        return self.__clinica

    @clinica.setter
    def clinica(self, valor: Clinica):
        self.__clinica = valor

    @property
    def paciente(self) -> Paciente:
        return self.__paciente

    @paciente.setter
    def paciente(self, valor: Paciente):
        self.__paciente = valor

    @property
    def profissional(self) -> Profissional:
        return self.__profissional

    @profissional.setter
    def profissional(self, valor: Profissional):
        self.__profissional = valor

    @property
    def data(self) -> Date:
        return self.__data

    @data.setter
    def data(self, valor: Date):
        self.__data = valor

    @property
    def hora_inicio(self) -> Time:
        return self.__hora_inicio

    @hora_inicio.setter
    def hora_inicio(self, valor: Time):
        self.__hora_inicio = valor

    @property
    def hora_fim(self) -> Time:
        return self.__hora_fim

    @hora_fim.setter
    def hora_fim(self, valor: Time):
        self.__hora_fim = valor

    @property
    def tipo_atendimento(self) -> TipoAtendimento:
        return self.__tipo_atendimento

    @tipo_atendimento.setter
    def tipo_atendimento(self, valor: TipoAtendimento):
        self.__tipo_atendimento = valor

    @property
    def valor(self) -> float:
        return self.__valor

    @valor.setter
    def valor(self, valor: float):
        self.__valor = valor

    @property
    def numero_atendimento(self) -> int:
        return self.__numero_atendimento

    @numero_atendimento.setter
    def numero_atendimento(self, valor: int):
        self.__numero_atendimento = valor

    @property
    def acompanhante(self) -> Acompanhante:
        return self.__acompanhante

    @acompanhante.setter
    def acompanhante(self, valor: Acompanhante):
        self.__acompanhante = valor

    @property
    def pagamentos(self) -> list:
        return self.__pagamentos

    @property
    def procedimentos(self) -> list:
        return self.__procedimentos

    @property
    def valor_total(self) -> float:
        return self.valor + sum(
            procedimento.custo
            for procedimento in self.__procedimentos
        )

    def total_pago(self) -> float:
        return sum(
            pagamento.valor_pagamento
            for pagamento in self.__pagamentos
        )

    def pago(self) -> bool:
        return self.total_pago() >= self.valor_total

    def mostra_valor_restante(self) -> float:
        return max(
            0.0, self.valor_total - self.total_pago()
        )

    def adiciona_pagamento(self, pagamento):
        self.__pagamentos.append(pagamento)

    def remove_pagamento(self, pagamento) -> None:
        if pagamento in self.__pagamentos:
            self.__pagamentos.remove(pagamento)

    def inclui_procedimento(self, procedimento: Procedimento):
        self.__procedimentos.append(procedimento)

    def remove_procedimento(self, procedimento: Procedimento) -> None:
        if procedimento in self.__procedimentos:
            self.__procedimentos.remove(procedimento)

    def mostra_dados(self) -> str:
        return (
            f"Atendimento Nº {self.numero_atendimento} - "
            f"Paciente: {self.paciente.nome}, "
            f"Profissional: {self.profissional.nome}, "
            f"Data: {self.data:%d/%m/%Y}, "
            f"Horário: {self.hora_inicio:%H:%M} às "
            f"{self.hora_fim:%H:%M}, "
            f"Tipo: {self.tipo_atendimento.nome}, "
            f"Valor Total: R$ {self.valor_total:.2f}, "
            f"Pago: {'Sim' if self.pago() else 'Não'}, "
            f"Restante: R$ {self.mostra_valor_restante():.2f}"
        )
