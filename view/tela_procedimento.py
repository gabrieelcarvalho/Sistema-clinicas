
class TelaProcedimento:
    def tela_opcoes(self) -> int:
        print("\n=== GERENCIAR PROCEDIMENTOS ===")
        print("1 - Cadastrar Procedimento")
        print("2 - Excluir Procedimento")
        print("3 - Alterar Descrição")
        print("4 - Alterar Custo")
        print("5 - Alterar Profissional")
        print("6 - Listar Procedimentos")
        print("0 - Retornar")

        try:
            return int(input("Escolha a opção: "))
        except ValueError:
            return -1

    def pega_novo_dado(self, campo: str) -> str:
        return input(f"Novo(a) {campo}: ").strip()

    def pega_custo(self) -> float:
        while True:
            try:
                custo = float(
                    input("Custo (R$): ").strip()
                )

                if 0 <= custo < float("inf"):
                    return custo

                print(
                    "[AVISO]: Informe um custo "
                    "não negativo e finito!"
                )

            except ValueError:
                print("[AVISO]: Custo inválido!")

    def pega_dados_procedimento(self) -> dict:
        print("\n--- Dados do Procedimento ---")

        return {
            "descricao": input(
                "Descrição: "
            ).strip(),
            "custo": self.pega_custo()
        }

    def seleciona_procedimento(self) -> str:
        return input(
            "Descrição do procedimento: "
        ).strip()

    def seleciona_profissional(self) -> str:
        return input(
            "CPF do profissional responsável: "
        ).strip()

    def mostra_procedimento(self, dados: dict) -> None:
        print(
            f"Descrição: {dados['descricao']} | "
            f"Custo: R$ {dados['custo']:.2f} | "
            f"Profissional: {dados['profissional']}"
        )

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")
