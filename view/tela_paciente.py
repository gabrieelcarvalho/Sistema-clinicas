import re
from datetime import datetime, date


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


class TelaPaciente:
    def tela_opcoes(self) -> int:
        print("\n=== GERENCIAR PACIENTES ===")
        print("1 - Cadastrar Paciente")
        print("2 - Excluir Paciente")
        print("3 - Alterar Nome")
        print("4 - Alterar CPF")
        print("5 - Listar Pacientes")
        print("6 - Alterar Celular")
        print("7 - Alterar Data de Nascimento")
        print("0 - Retornar")

        try:
            return int(input("Escolha a opção: "))
        except ValueError:
            return -1

    def pega_nova_data_nascimento(self) -> date:
        while True:
            try:
                nascimento = input(
                    "Data de nascimento (DD/MM/AAAA): "
                ).strip()

                data = datetime.strptime(
                    nascimento, "%d/%m/%Y"
                ).date()

                if data > date.today():
                    print("[AVISO]: A data não pode ser futura!")
                    continue

                return data

            except ValueError:
                print("[AVISO]: Data inválida!")

    def pega_dados_paciente(self) -> dict:
        print("\n--- Dados do Paciente ---")

        nome = input("Nome: ").strip()
        cpf = solicitar_cpf()
        celular = solicitar_celular()
        data_nascimento = self.pega_nova_data_nascimento()

        return {
            "nome": nome,
            "cpf": cpf,
            "celular": celular,
            "data_nascimento": data_nascimento
        }

    def pega_novo_dado(self, campo: str) -> str:
        if campo == "cpf":
            return solicitar_cpf("Novo CPF")

        if campo == "celular":
            return solicitar_celular("Novo celular")

        return input(f"Novo(a) {campo}: ").strip()

    def mostra_paciente(self, dados: dict) -> None:
        print(
            f"Nome: {dados['nome']} | "
            f"CPF: {dados['cpf']} | "
            f"Celular: {dados['celular']} | "
            f"Nascimento: {dados['data_nascimento']:%d/%m/%Y}"
        )

    def seleciona_paciente(self) -> str:
        return solicitar_cpf("CPF do paciente")

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")
