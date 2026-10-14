from datetime import datetime

class TelaPaciente:
    def tela_opcoes(self) -> int:
        print("\n" + "=" * 35)
        print("        GERENCIAR PACIENTES")
        print("=" * 35)
        print("1 - Cadastrar Paciente")
        print("2 - Excluir Paciente")
        print("3 - Alterar Nome")
        print("4 - Alterar CPF")
        print("5 - Listar Pacientes")
        print("6 - Alterar Data de Nascimento")
        print("0 - Retornar")
        print("=" * 35)

        try:
            return int(input("Escolha a opção: "))
        except ValueError:
            return -1

    def pega_dados_paciente(self) -> dict:
    print("\n--- Dados do Paciente ---")
    nome = input("Nome: ").strip()
    cpf = input("CPF: ").strip()
    celular = input("Celular: ").strip()

    while True:
        try:
            nascimento = input(
                "Data de nascimento (DD/MM/AAAA): "
            ).strip()
            data_nascimento = datetime.strptime(
                nascimento, "%d/%m/%Y"
            ).date()

            if data_nascimento > datetime.today().date():
                print("[AVISO]: A data não pode ser futura!")
                continue

            break
        except ValueError:
            print("[AVISO]: Data inválida! Use DD/MM/AAAA.")

    return {
        "nome": nome,
        "cpf": cpf,
        "celular": celular,
        "data_nascimento": data_nascimento
    }

    def mostra_paciente(self, dados: dict) -> None:
    print(
        f"Nome: {dados['nome']} | "
        f"CPF: {dados['cpf']} | "
        f"Celular: {dados['celular']} | "
        f"Nascimento: {dados['data_nascimento'].strftime('%d/%m/%Y')}"
    )

    def seleciona_paciente(self) -> str:
        return input("Digite o CPF do paciente: ").strip()

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")

    def pega_nova_data_nascimento(self):
    while True:
        try:
            texto = input(
                "Nova data de nascimento (DD/MM/AAAA): "
            ).strip()

            data = datetime.strptime(texto, "%d/%m/%Y").date()

            if data > datetime.today().date():
                print("[AVISO]: A data não pode ser futura!")
                continue

            return data

        except ValueError:
            print("[AVISO]: Data inválida!")