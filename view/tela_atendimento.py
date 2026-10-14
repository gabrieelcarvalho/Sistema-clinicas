from datetime import datetime


class TelaAtendimento:
    def tela_opcoes(self) -> int:
        print("\n" + "=" * 35)
        print("      GERENCIAR ATENDIMENTOS")
        print("=" * 35)
        print("1 - Agendar Atendimento")
        print("2 - Reagendar Atendimento")
        print("3 - Cancelar Atendimento")
        print("4 - Incluir Procedimento no Atendimento")
        print("5 - Registrar Pagamento")
        print("6 - Listar Atendimentos")
        print("0 - Retornar")
        print("=" * 35)

        try:
            opcao = int(input("Escolha a opção: "))
            return opcao
        except ValueError:
            return -1

    def pega_dados_agendamento(self) -> dict:
        print("\n--- Dados do Agendamento ---")
        while True:
            try:
                numero_atendimento = int(input("Número do Atendimento: ").strip())
                break
            except ValueError:
                print("\n[AVISO]: O número do atendimento deve ser inteiro!")

        nome_clinica = input("Nome da Clínica: ").strip()
        cpf_paciente = input("CPF do Paciente: ").strip()
        cpf_profissional = input("CPF do Profissional: ").strip()

        while True:
            try:
                codigo_tipo = int(input("Código do Tipo de Atendimento: ").strip())
                break
            except ValueError:
                print("\n[AVISO]: Digite um código numérico inteiro!")

        while True:
            try:
                data_str = input("Data do Atendimento (DD/MM/AAAA): ").strip()
                data = datetime.strptime(data_str, "%d/%m/%Y").date()
                break
            except ValueError:
                print("\n[AVISO]: Data inválida! Use o formato DD/MM/AAAA.")

        while True:
            try:
                ini_str = input("Horário de Início (HH:MM): ").strip()
                hora_inicio = datetime.strptime(ini_str, "%H:%M").time()
                fim_str = input("Horário de Fim (HH:MM): ").strip()
                hora_fim = datetime.strptime(fim_str, "%H:%M").time()
                if hora_fim > hora_inicio:
                    break
                print("\n[AVISO]: O horário de fim deve ser maior que o de início!")
            except ValueError:
                print("\n[AVISO]: Horário inválido! Use o formato HH:MM.")

        while True:
            try:
                valor = float(input("Valor da Consulta/Atendimento (R$): ").strip())
                if valor >= 0:
                    break
                print("\n[AVISO]: O valor não pode ser negativo!")
            except ValueError:
                print("\n[AVISO]: Digite um valor numérico válido!")

        return {
            "numero_atendimento": numero_atendimento,
            "nome_clinica": nome_clinica,
            "cpf_paciente": cpf_paciente,
            "cpf_profissional": cpf_profissional,
            "codigo_tipo": codigo_tipo,
            "data": data,
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim,
            "valor": valor,
        }

    def seleciona_forma_pagamento(self) -> int:
        print("\n--- Forma de Pagamento ---")
        print("1 - Dinheiro")
        print("2 - PIX")
        print("3 - Cartão de Crédito")
        try:
            return int(input("Escolha a modalidade: ").strip())
        except ValueError:
            return -1

    def pega_dados_pix(self) -> dict:
        print("\n--- Pagamento via PIX ---")
        while True:
            try:
                data_str = input("Data do Pagamento (DD/MM/AAAA): ").strip()
                data = datetime.strptime(data_str, "%d/%m/%Y").date()
                valor = float(input("Valor Pago (R$): ").strip())
                break
            except ValueError:
                print("\n[AVISO]: Data ou valor inválidos!")
        cpf = input("CPF do Pagador: ").strip()
        return {"data": data, "valor_pagamento": valor, "cpf": cpf}

    def pega_dados_cartao(self) -> dict:
        print("\n--- Pagamento via Cartão de Crédito ---")
        while True:
            try:
                data_str = input("Data do Pagamento (DD/MM/AAAA): ").strip()
                data = datetime.strptime(data_str, "%d/%m/%Y").date()
                valor = float(input("Valor Pago (R$): ").strip())
                parcelas = int(input("Número de Parcelas: ").strip())
                break
            except ValueError:
                print("\n[AVISO]: Dados inválidos! Verifique data, valor ou parcelas.")
        bandeira = input("Bandeira do Cartão: ").strip()
        numero = input("Número do Cartão: ").strip()
        return {
            "data": data,
            "valor_pagamento": valor,
            "bandeira": bandeira,
            "numero": numero,
            "parcelas": parcelas,
        }

    def pega_dados_dinheiro(self) -> dict:
        print("\n--- Pagamento em Dinheiro ---")
        while True:
            try:
                data_str = input("Data do Pagamento (DD/MM/AAAA): ").strip()
                data = datetime.strptime(data_str, "%d/%m/%Y").date()
                valor = float(input("Valor Pago (R$): ").strip())
                break
            except ValueError:
                print("\n[AVISO]: Data ou valor inválidos!")
        return {"data": data, "valor_pagamento": valor}

    def pega_dados_acompanhante(self) -> dict:
        print("\n--- Dados do Acompanhante ---")
        nome = input("Nome do Acompanhante: ").strip()
        cpf = input("CPF do Acompanhante: ").strip()
        celular = input("Celular do Acompanhante: ").strip()
        while True:
            try:
                nasc_str = input("Data de Nascimento (DD/MM/AAAA): ").strip()
                data_nascimento = datetime.strptime(nasc_str, "%d/%m/%Y").date()
                break
            except ValueError:
                print("\n[AVISO]: Data inválida! Use DD/MM/AAAA.")
        relacao = input("Relação com o Paciente: ").strip()
        return {
            "nome": nome,
            "cpf": cpf,
            "celular": celular,
            "data_nascimento": data_nascimento,
            "relacao_paciente": relacao,
        }

    def mostra_atendimento(self, dados: dict) -> None:
        print(
            f"Nº: {dados['numero_atendimento']} | Clínica: {dados['clinica']} | "
            f"Paciente: {dados['paciente']} | Profissional: {dados['profissional']} | "
            f"Data: {dados['data']} ({dados['hora_inicio']} às {dados['hora_fim']}) | "
            f"Tipo: {dados['tipo']} | Valor Total: R$ {dados['valor_total']:.2f} | "
            f"Restante: R$ {dados['valor_restante']:.2f} | Pago: {dados['pago']}"
        )

    def seleciona_atendimento(self) -> int:
        while True:
            try:
                return int(input("Digite o Número do Atendimento: ").strip())
            except ValueError:
                print("\n[AVISO]: Digite um número inteiro válido!")

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")