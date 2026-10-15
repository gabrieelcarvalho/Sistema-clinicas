from datetime import datetime, date as Date, time as Time


class TelaAtendimento:
    def mostra_mensagem(self, mensagem: str) -> None:
        print(mensagem)

    def pega_int(self, mensagem: str) -> int:
        while True:
            try:
                return int(input(f"{mensagem}: "))
            except ValueError:
                print("Valor inválido! Digite um número inteiro.")

    def pega_float(self, mensagem: str) -> float:
        while True:
            try:
                return float(input(f"{mensagem}: "))
            except ValueError:
                print("Valor inválido! Digite um número decimal.")

    def pega_data(self, mensagem: str) -> Date:
        while True:
            data_str = input(f"{mensagem}: ").strip()
            try:
                return datetime.strptime(data_str, "%d/%m/%Y").date()
            except ValueError:
                print("Data inválida! Use o formato DD/MM/AAAA.")

    def pega_horario(self, mensagem: str) -> Time:
        while True:
            hora_str = input(f"{mensagem}: ").strip()
            try:
                return datetime.strptime(hora_str, "%H:%M").time()
            except ValueError:
                print("Horário inválido! Use o formato HH:MM.")

    def tela_opcoes(self) -> int:
        print("\n" + "=" * 40)
        print("         MENU DE ATENDIMENTOS")
        print("=" * 40)
        print("1  - Agendar Atendimento")
        print("2  - Reagendar Atendimento")
        print("3  - Cancelar Atendimento")
        print("4  - Incluir Procedimento em Atendimento")
        print("5  - Registrar Pagamento")
        print("6  - Listar Atendimentos")
        print("7  - Listar Pagamentos de Atendimento")
        print("8  - Alterar Pagamento de Atendimento")
        print("9  - Excluir Pagamento de Atendimento")
        print("10 - Listar Procedimentos de Atendimento")
        print("11 - Excluir Procedimento de Atendimento")
        print("12 - Alterar Dados do Atendimento")
        print("0  - Voltar")
        return self.pega_int("Escolha uma opção")

    def pega_dados_agendamento(self) -> dict:
        print("\n--- Dados do Agendamento ---")
        nome_clinica = input("Nome da clínica: ").strip()
        cpf_paciente = input("CPF do paciente: ").strip()
        cpf_profissional = input("CPF do profissional: ").strip()
        codigo_tipo = self.pega_int("Código do tipo de atendimento")
        data = self.pega_data("Data do atendimento (DD/MM/AAAA)")
        hora_inicio = self.pega_horario("Horário de início (HH:MM)")
        hora_fim = self.pega_horario("Horário de término (HH:MM)")
        valor = self.pega_float("Valor base do atendimento (R$)")

        return {
            "nome_clinica": nome_clinica,
            "cpf_paciente": cpf_paciente,
            "cpf_profissional": cpf_profissional,
            "codigo_tipo": codigo_tipo,
            "data": data,
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim,
            "valor": valor
        }

    def pega_dados_acompanhante(self) -> dict:
        print("\n--- Dados do Acompanhante ---")
        cpf = input("CPF do acompanhante: ").strip()
        nome = input("Nome do acompanhante: ").strip()
        celular = input("Celular do acompanhante: ").strip()
        data_nascimento = self.pega_data("Data de nascimento (DD/MM/AAAA)")

        return {
            "cpf": cpf,
            "nome": nome,
            "celular": celular,
            "data_nascimento": data_nascimento
        }

    def seleciona_atendimento(self) -> int:
        return self.pega_int("Número do atendimento")

    def pega_dados_reagendamento(self) -> dict:
        print("\n--- Reagendamento de Atendimento ---")
        data = self.pega_data("Nova data (DD/MM/AAAA)")
        hora_inicio = self.pega_horario("Novo horário de início (HH:MM)")
        hora_fim = self.pega_horario("Novo horário de término (HH:MM)")

        return {
            "data": data,
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim
        }

    def seleciona_procedimento(self) -> str:
        return input("Descrição do procedimento: ").strip()

    def seleciona_forma_pagamento(self) -> int:
        print("\n--- Forma de Pagamento ---")
        print("1 - Dinheiro")
        print("2 - Pix")
        print("3 - Cartão")
        return self.pega_int("Escolha a forma de pagamento")

    def pega_dados_dinheiro(self) -> dict:
        data = self.pega_data("Data do pagamento (DD/MM/AAAA)")
        valor = self.pega_float("Valor do pagamento (R$)")
        return {
            "data": data,
            "valor_pagamento": valor
        }

    def pega_dados_pix(self) -> dict:
        data = self.pega_data("Data do pagamento (DD/MM/AAAA)")
        valor = self.pega_float("Valor do pagamento (R$)")
        cpf = input("CPF do pagador: ").strip()
        return {
            "data": data,
            "valor_pagamento": valor,
            "cpf": cpf
        }

    def pega_dados_cartao(self) -> dict:
        data = self.pega_data("Data do pagamento (DD/MM/AAAA)")
        valor = self.pega_float("Valor do pagamento (R$)")
        bandeira = input("Bandeira do cartão: ").strip()
        numero = input("Número do cartão: ").strip()

        return {
            "data": data,
            "valor_pagamento": valor,
            "bandeira": bandeira,
            "numero": numero
        }

    def mostra_atendimento(self, dados: dict) -> None:
        print("\n----------------------------------------")
        print(f"Número do Atendimento: {dados['numero_atendimento']}")
        print(f"Clínica: {dados['clinica']}")
        print(f"Paciente: {dados['paciente']}")
        print(f"Profissional: {dados['profissional']}")
        print(f"Data: {dados['data']}")
        print(f"Horário: {dados['hora_inicio']} - {dados['hora_fim']}")
        print(f"Tipo: {dados['tipo']}")
        print(f"Valor Total: R$ {dados['valor_total']:.2f}")
        print(f"Valor Restante: R$ {dados['valor_restante']:.2f}")
        print(f"Pago: {dados['pago']}")
        print("----------------------------------------")

    def mostra_pagamentos(self, pagamentos: list) -> None:
        print("\n--- Lista de Pagamentos ---")
        for i, item in enumerate(pagamentos):
            print(f"[{i}] {item}")

    def mostra_procedimentos(self, procedimentos: list) -> None:
        print("\n--- Lista de Procedimentos ---")
        for i, item in enumerate(procedimentos):
            print(f"[{i}] {item}")

    def seleciona_indice(self, label: str) -> int:
        return self.pega_int(f"Informe o {label}")

    def pega_dados_alteracao_pagamento(self) -> dict:
        valor = self.pega_float("Novo valor do pagamento (R$)")
        return {"valor": valor}

    def pega_dados_alteracao(self) -> dict:
        print("\n--- Alterar Dados do Atendimento ---")
        cpf_profissional = input("Novo CPF do profissional (ou Enter para manter): ").strip()
        codigo_tipo_str = input("Novo código do tipo de atendimento (ou Enter para manter): ").strip()
        valor_str = input("Novo valor base do atendimento (ou Enter para manter): ").strip()

        codigo_tipo = int(codigo_tipo_str) if codigo_tipo_str.isdigit() else None
        valor = float(valor_str) if valor_str else None

        return {
            "cpf_profissional": cpf_profissional if cpf_profissional else None,
            "codigo_tipo": codigo_tipo,
            "valor": valor
        }