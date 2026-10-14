
class TelaTipoAtendimento:
    def tela_opcoes(self) -> int:
        print("\n=== GERENCIAR TIPOS DE ATENDIMENTO ===")
        print("1 - Cadastrar Tipo")
        print("2 - Alterar Tipo")
        print("3 - Listar Tipos")
        print("4 - Excluir Tipo")
        print("0 - Retornar")

        try:
            return int(input("Escolha a opção: "))
        except ValueError:
            return -1

    def seleciona_tipo(self) -> int:
        while True:
            try:
                return int(
                    input(
                        "Código do tipo de atendimento: "
                    ).strip()
                )
            except ValueError:
                print(
                    "[AVISO]: Informe um número inteiro!"
                )

    def pega_dados_tipo(self) -> dict:
        print("\n--- Dados do Tipo ---")

        return {
            "codigo": self.seleciona_tipo(),
            "nome": input("Nome: ").strip()
        }

    def pega_novo_dado(self, campo: str) -> str:
        return input(f"Novo(a) {campo}: ").strip()

    def mostra_tipo(self, dados: dict) -> None:
        print(
            f"Código: {dados['codigo']} | "
            f"Nome: {dados['nome']}"
        )

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")
