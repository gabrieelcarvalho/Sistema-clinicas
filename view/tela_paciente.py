
from datetime import datetime, date


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
        cpf = input("CPF: ").strip()
        celular = input("Celular: ").strip()
        data_nascimento = self.pega_nova_data_nascimento()

        return {
            "nome": nome,
            "cpf": cpf,
            "celular": celular,
            "data_nascimento": data_nascimento
        }

    def pega_novo_dado(self, campo: str) -> str:
        return input(f"Novo(a) {campo}: ").strip()

    def mostra_paciente(self, dados: dict) -> None:
        print(
            f"Nome: {dados['nome']} | "
            f"CPF: {dados['cpf']} | "
            f"Celular: {dados['celular']} | "
            f"Nascimento: {dados['data_nascimento']:%d/%m/%Y}"
        )

    def seleciona_paciente(self) -> str:
        return input("CPF do paciente: ").strip()

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")
