class TelaPaciente:
    def tela_opcoes(self) -> int:
        print("\n" + "=" * 35)
        print("        GERENCIAR PACIENTES")
        print("=" * 35)
        print("1 - Cadastrar Paciente")
        print("2 - Excluir Paciente")
        print("3 - Alterar Nome")
        print("4 - Alterar CPF")
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

        return {
            "nome": nome,
            "cpf": cpf,
            "celular": celular,
        }

    def mostra_paciente(self, dados: dict) -> None:
        print(f"Nome: {dados['nome']} | CPF: {dados['cpf']} | Celular: {dados['celular']}")

    def seleciona_paciente(self) -> str:
        return input("Digite o CPF do paciente: ").strip()

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")