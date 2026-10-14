
class TelaProfissional:
    def tela_opcoes(self) -> int:
        print("\n=== GERENCIAR PROFISSIONAIS ===")
        print("1 - Cadastrar Profissional")
        print("2 - Excluir Profissional")
        print("3 - Alterar Especialidade")
        print("4 - Alterar Registro Profissional")
        print("5 - Alterar Nome")
        print("6 - Alterar CPF")
        print("7 - Listar Profissionais")
        print("8 - Alterar Celular")
        print("0 - Retornar")

        try:
            return int(input("Escolha a opção: "))
        except ValueError:
            return -1

    def pega_dados_profissional(self) -> dict:
        print("\n--- Dados do Profissional ---")

        return {
            "nome": input("Nome: ").strip(),
            "cpf": input("CPF: ").strip(),
            "celular": input("Celular: ").strip(),
            "especialidade": input("Especialidade: ").strip(),
            "registro_profissional": input(
                "Registro Profissional: "
            ).strip()
        }

    def pega_novo_dado(self, campo: str) -> str:
        return input(f"Novo(a) {campo}: ").strip()

    def mostra_profissional(self, dados: dict) -> None:
        print(
            f"Nome: {dados['nome']} | "
            f"CPF: {dados['cpf']} | "
            f"Celular: {dados['celular']} | "
            f"Especialidade: {dados['especialidade']} | "
            f"Registro: {dados['registro_profissional']}"
        )

    def seleciona_profissional(
        self, tipo: str = "CPF"
    ) -> str:
        return input(
            f"Digite o {tipo} do profissional: "
        ).strip()

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")
