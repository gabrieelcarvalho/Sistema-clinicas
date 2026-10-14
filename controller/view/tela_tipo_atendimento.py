class TelaTipoAtendimento:
    def tela_opcoes(self) -> int:
        print("\n" + "=" * 35)
        print("   GERENCIAR TIPOS DE ATENDIMENTO")
        print("=" * 35)
        print("1 - Cadastrar Tipo de Atendimento")
        print("2 - Alterar Tipo de Atendimento")
        print("3 - Listar Tipos de Atendimento")
        print("4 - Excluir Tipo de Atendimento")
        print("0 - Retornar")
        print("=" * 35)

        try:
            opcao = int(input("Escolha a opção: "))
            return opcao
        except ValueError:
            return -1

    def pega_dados_tipo(self) -> dict:
        print("\n--- Dados do Tipo de Atendimento ---")
        while True:
            try:
                codigo = int(input("Código (número inteiro): ").strip())
                break
            except ValueError:
                print("\n[AVISO]: O código deve ser um número inteiro!")

        nome = input("Nome do Tipo de Atendimento: ").strip()
        return {"codigo": codigo, "nome": nome}

    def mostra_tipo(self, dados: dict) -> None:
        print(f"Código: {dados['codigo']} | Nome: {dados['nome']}")

    def seleciona_tipo(self) -> int:
        while True:
            try:
                return int(input("Digite o código do Tipo de Atendimento: ").strip())
            except ValueError:
                print("\n[AVISO]: Digite um código numérico inteiro válido!")

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")