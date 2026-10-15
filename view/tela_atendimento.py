import re
from datetime import datetime


def solicitar_cpf(campo: str = "CPF", opcional: bool = False) -> str:
    while True:
        cpf = input(f"{campo} (000.000.000-00): ").strip()

        if opcional and not cpf:
            return ""

        if re.fullmatch(r"[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}", cpf):
            return cpf

        print("[AVISO]: CPF inválido! Use 000.000.000-00.")


def solicitar_celular(campo: str = "Celular") -> str:
    while True:
        celular = input(f"{campo} ((00) 00000-0000): ").strip()

        if re.fullmatch(r"\([0-9]{2}\) [0-9]{5}-[0-9]{4}", celular):
            return celular

        print("[AVISO]: Celular inválido! Use (00) 00000-0000.")


class TelaAtendimento:
    def tela_opcoes(self) -> int:
        print("\n=== GERENCIAR ATENDIMENTOS ===")
        print("1 - Agendar")
        print("2 - Reagendar")
        print("3 - Cancelar")
        print("4 - Incluir Procedimento")
        print("5 - Registrar Pagamento")
        print("6 - Listar Atendimentos")
        print("7 - Listar Pagamentos")
        print("8 - Alterar Pagamento")
        print("9 - Excluir Pagamento")
        print("10 - Listar Procedimentos Vinculados")
        print("11 - Excluir Procedimento Vinculado")
        print("12 - Alterar Profissional, Tipo ou Valor")
        print("0 - Retornar")

        try:
            return int(input("Escolha a opção: "))
        except ValueError:
            return -1

    def pega_novo_dado(self, campo: str) -> str:
        return input(f"Novo(a) {campo}: ").strip()

    def pega_inteiro(self, campo: str) -> int:
        while True:
            try:
                return int(
                    input(f"{campo}: ").strip()
                )
            except ValueError:
                print(
                    "[AVISO]: Informe um número inteiro!"
                )

    def pega_valor(self, campo: str) -> float:
        while True:
            try:
                valor = float(
                    input(f"{campo} (R$): ").strip()
                )

                if 0 <= valor < float("inf"):
                    return valor

                print(
                    "[AVISO]: Valor não pode ser "
                    "negativo ou infinito!"
                )

            except ValueError:
                print("[AVISO]: Valor inválido!")

    def pega_data(self, campo: str):
        while True:
            try:
                texto = input(
                    f"{campo} (DD/MM/AAAA): "
                ).strip()

                return datetime.strptime(
                    texto, "%d/%m/%Y"
                ).date()

            except ValueError:
                print("[AVISO]: Data inválida!")

    def pega_horario(self, campo: str):
        while True:
            try:
                texto = input(
                    f"{campo} (HH:MM): "
                ).strip()

                return datetime.strptime(
                    texto, "%H:%M"
                ).time()

            except ValueError:
                print("[AVISO]: Horário inválido!")

    def pega_periodo(self) -> dict:
        while True:
            inicio = self.pega_horario(
                "Horário de início"
            )
            fim = self.pega_horario(
                "Horário de fim"
            )

            if inicio < fim:
                return {
                    "hora_inicio": inicio,
                    "hora_fim": fim
                }

            print(
                "[AVISO]: Fim deve ser posterior ao início!"
            )

    def pega_dados_agendamento(self) -> dict:
        print("\n--- Dados do Atendimento ---")

        dados = {
            "numero_atendimento": self.pega_inteiro(
                "Número do atendimento"
            ),
            "nome_clinica": input(
                "Nome da clínica: "
            ).strip(),
            "cpf_paciente": solicitar_cpf(
                "CPF do paciente"
            ),
            "cpf_profissional": solicitar_cpf(
                "CPF do profissional"
            ),
            "codigo_tipo": self.pega_inteiro(
                "Código do tipo"
            ),
            "data": self.pega_data(
                "Data do atendimento"
            )
        }

        dados.update(self.pega_periodo())
        dados["valor"] = self.pega_valor(
            "Valor do atendimento"
        )

        return dados

    def pega_dados_reagendamento(self) -> dict:
        dados = {
            "data": self.pega_data("Nova data")
        }

        dados.update(self.pega_periodo())
        return dados

    def pega_dados_alteracao(self) -> dict:
        print(
            "Deixe CPF e tipo vazios para "
            "manter os dados atuais."
        )

        cpf = solicitar_cpf(
            "Novo CPF do profissional",
            opcional=True
        )

        texto_tipo = input(
            "Novo código do tipo (opcional): "
        ).strip()

        print(
            "Valor do atendimento: deixe em "
            "branco para não alterar."
        )

        while True:
            texto_valor = input(
                "Novo valor (opcional): "
            ).strip()

            if not texto_valor:
                valor = None
                break

            try:
                valor = float(texto_valor)
                if 0 <= valor < float("inf"):
                    break
            except ValueError:
                pass

            print("[AVISO]: Valor inválido!")

        while texto_tipo and not texto_tipo.isdecimal():
            print(
                "[AVISO]: Informe um código inteiro "
                "não negativo!"
            )
            texto_tipo = input(
                "Novo código do tipo (opcional): "
            ).strip()

        return {
            "cpf_profissional": cpf,
            "codigo_tipo": (
                int(texto_tipo) if texto_tipo else None
            ),
            "valor": valor
        }

    def seleciona_forma_pagamento(self) -> int:
        print("1 - Dinheiro")
        print("2 - PIX")
        print("3 - Cartão de crédito")

        return self.pega_inteiro("Modalidade")

    def pega_dados_dinheiro(self) -> dict:
        return {
            "data": self.pega_data("Data do pagamento"),
            "valor_pagamento": self.pega_valor("Valor pago")
        }

    def pega_dados_pix(self) -> dict:
        dados = self.pega_dados_dinheiro()
        dados["cpf"] = solicitar_cpf(
            "CPF do pagador"
        )
        return dados

    def pega_dados_cartao(self) -> dict:
        dados = self.pega_dados_dinheiro()
        dados["bandeira"] = input(
            "Bandeira: "
        ).strip()
        dados["numero"] = input(
            "Número do cartão: "
        ).strip()
        dados["parcelas"] = self.pega_inteiro(
            "Quantidade de parcelas"
        )
        return dados

    def pega_dados_acompanhante(self) -> dict:
        print("\n--- Dados do Acompanhante ---")

        return {
            "cpf": solicitar_cpf(),
            "nome": input("Nome: ").strip(),
            "celular": solicitar_celular(),
            "data_nascimento": self.pega_data(
                "Nascimento"
            ),
            "relacao_paciente": input(
                "Relação com o paciente: "
            ).strip()
        }

    def seleciona_atendimento(self) -> int:
        return self.pega_inteiro(
            "Número do atendimento"
        )

    def seleciona_procedimento(self) -> str:
        return input(
            "Descrição do procedimento: "
        ).strip()

    def seleciona_indice(self, titulo: str) -> int:
        return self.pega_inteiro(titulo) - 1

    def mostra_atendimento(self, dados: dict) -> None:
        print(
            f"Nº {dados['numero_atendimento']} | "
            f"Clínica: {dados['clinica']} | "
            f"Paciente: {dados['paciente']} | "
            f"Profissional: {dados['profissional']} | "
            f"Data: {dados['data']} "
            f"({dados['hora_inicio']} às {dados['hora_fim']}) | "
            f"Tipo: {dados['tipo']} | "
            f"Total: R$ {dados['valor_total']:.2f} | "
            f"Restante: R$ {dados['valor_restante']:.2f} | "
            f"Pago: {dados['pago']}"
        )

    def mostra_pagamentos(self, dados: list) -> None:
        print("\n--- PAGAMENTOS ---")

        if not dados:
            print("Nenhum pagamento registrado.")

        for indice, descricao in enumerate(
            dados, start=1
        ):
            print(f"{indice} - {descricao}")

    def mostra_procedimentos(self, dados: list) -> None:
        print("\n--- PROCEDIMENTOS VINCULADOS ---")

        if not dados:
            print("Nenhum procedimento registrado.")

        for indice, descricao in enumerate(
            dados, start=1
        ):
            print(f"{indice} - {descricao}")

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")