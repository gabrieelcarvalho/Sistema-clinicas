class TelaProfissional:
    def tela_opcoes(self) -> int:
        print("\n" + "=" * 35)
        print("      GERENCIAR PROFISSIONAIS")
        print("=" * 35)
        print("1 - Cadastrar Profissional")
        print("2 - Excluir Profissional")
        print("3 - Alterar Especialidade")
        print("4 - Alterar Registro Profissional")
        print("5 - Alterar Nome")
        print("6 - Alterar CPF")
        print("0 - Retornar")
        print("=" * 35)

        try:
            return int(input("Escolha a opção: "))
        except ValueError:
            return -1

    def pega_dados_profissional(self) -> dict:
        print("\n--- Dados do Profissional ---")
        nome = input("Nome: ").strip()
        cpf = input("CPF: ").strip()
        celular = input("Celular: ").strip()
        especialidade = input("Especialidade: ").strip()
        registro = input("Registro Profissional: ").strip()

        return {
            "nome": nome,
            "cpf": cpf,
            "celular": celular,
            "especialidade": especialidade,
            "registro_profissional": registro,
        }

    def mostra_profissional(self, dados: dict) -> None:
        print(
            f"Nome: {dados['nome']} | CPF: {dados['cpf']} | "
            f"Celular: {dados['celular']} | Especialidade: {dados['especialidade']} | "
            f"Registro: {dados['registro_profissional']}"
        )

    def seleciona_profissional(self) -> str:
        return input("Digite o identificador do profissional (CPF ou Registro): ").strip()

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")