from datetime import date as Date, time as Time
from model.clinica import Clinica
from model.paciente import Paciente
from model.profissional import Profissional
from model.acompanhante import Acompanhante
from model.tipo_atendimento import TipoAtendimento
from model.procedimento import Procedimento


class Atendimento:
    def __init__(
        self,
        clinica: Clinica,
        paciente: Paciente,
        profissional: Profissional,
        data: Date,
        hora_inicio: Time,
        hora_fim: Time,
        tipo_atendimento: TipoAtendimento,
        valor: float,
        numero_atendimento: int,
        acompanhante: Acompanhante = None,
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
    def clinica(self, clinica: Clinica):
        self.__clinica = clinica

    @property
    def paciente(self) -> Paciente:
        return self.__paciente

    @paciente.setter
    def paciente(self, paciente: Paciente):
        self.__paciente = paciente

    @property
    def profissional(self) -> Profissional:
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional: Profissional):
        self.__profissional = profissional

    @property
    def data(self) -> Date:
        return self.__data

    @data.setter
    def data(self, data: Date):
        self.__data = data

    @property
    def hora_inicio(self) -> Time:
        return self.__hora_inicio

    @hora_inicio.setter
    def hora_inicio(self, hora_inicio: Time):
        self.__hora_inicio = hora_inicio

    @property
    def hora_fim(self) -> Time:
        return self.__hora_fim

    @hora_fim.setter
    def hora_fim(self, hora_fim: Time):
        self.__hora_fim = hora_fim

    @property
    def tipo_atendimento(self) -> TipoAtendimento:
        return self.__tipo_atendimento

    @tipo_atendimento.setter
    def tipo_atendimento(self, tipo_atendimento: TipoAtendimento):
        self.__tipo_atendimento = tipo_atendimento

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
    def numero_atendimento(self, numero_atendimento: int):
        self.__numero_atendimento = numero_atendimento

    @property
    def acompanhante(self) -> Acompanhante:
        return self.__acompanhante

    @acompanhante.setter
    def acompanhante(self, acompanhante: Acompanhante):
        self.__acompanhante = acompanhante

    @property
    def pagamentos(self) -> list:
        return self.__pagamentos

    @property
    def procedimentos(self) -> list:
        return self.__procedimentos

    @property
    def valor_total(self) -> float:
        total = self.valor
        for procedimento in self.__procedimentos:
            total += procedimento.custo
        return total

    def total_pago(self) -> float:
        total = 0.0
        for p in self.__pagamentos:
            # Se p for um objeto Pagamento com atributo valor, soma p.valor; se for float, soma p
            total += p.valor if hasattr(p, "valor") else p
        return total

    def pago(self) -> bool:
        return self.total_pago() >= self.valor_total

    def mostra_valor_restante(self) -> float:
        restante = self.valor_total - self.total_pago()
        return max(0.0, restante)

    def adiciona_pagamento(self, pagamento):
        self.__pagamentos.append(pagamento)

    def inclui_procedimento(self, procedimento: Procedimento):
        if procedimento not in self.__procedimentos:
            self.__procedimentos.append(procedimento)

    def mostra_dados(self) -> str:
        data_formatada = self.data.strftime("%d/%m/%Y")
        inicio_formatado = self.hora_inicio.strftime("%H:%M")
        fim_formatado = self.hora_fim.strftime("%H:%M")
        status_pago = "Sim" if self.pago() else "Não"
        
        return (
            f"Atendimento Nº {self.numero_atendimento} - Paciente: {self.paciente.nome}, "
            f"Profissional: {self.profissional.nome}, Data: {data_f}, Horário: {inicio_f} às {fim_f}, "
            f"Tipo: {self.tipo_atendimento.nome}, Valor Total: R$ {self.valor_total:.2f}, "
            f"Pago: {status_pago}, Restante: R$ {self.mostra_valor_restante():.2f}"
        )