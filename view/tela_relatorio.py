class TelaRelatorio:
    def tela_opcoes(self) -> int:
        print("\n" + "=" * 35)
        print("            RELATÓRIOS")
        print("=" * 35)
        print("1 - Clínicas com Maior Número de Atendimentos")
        print("2 - Atendimentos Mais Caros e Mais Baratos")
        print("3 - Procedimentos Mais Realizados (Populares)")
        print("4 - Procedimentos Mais Caros e Mais Baratos")
        print("0 - Retornar")
        print("=" * 35)

        try:
            opcao = int(input("Escolha a opção: "))
            return opcao
        except ValueError:
            return -1

    def mostra_relatorio(self, titulo: str, dados: list) -> None:
        print("\n" + "-" * 10 + f" {titulo} " + "-" * 10)
        for item in dados:
            print(item)
        print("-" * (22 + len(titulo)))

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")