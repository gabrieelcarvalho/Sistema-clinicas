class TelaProcedimento:
    def tela_opcoes(self) -> int:
        print("\n" + "=" * 35)
        print("      GERENCIAR PROCEDIMENTOS")
        print("=" * 35)
        print("1 - Cadastrar Procedimento")
        print("2 - Excluir Procedimento")
        print("0 - Retornar")
        print("=" * 35)

        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    def pega_dados_procedimento(self) -> dict:
        print("\n--- Dados do Procedimento ---")
        descricao = input("Descrição: ").strip()
        try:
            custo = float(input("Custo: ").strip())
        except ValueError:
            custo = 0.0

        return {
            "descricao": descricao,
            "custo": custo,
        }

    def mostra_procedimento(self, dados: dict) -> None:
        print(f"Descrição: {dados['descricao']} | Custo: R$ {dados['custo']:.2f}")

    def seleciona_procedimento(self) -> str:
        return input("Digite a descrição do procedimento: ").strip()

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")