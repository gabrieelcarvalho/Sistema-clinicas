class TelaSistema:
    def tela_opcoes(self) -> int:
        print("\n" + "=" * 35)
        print("      SISTEMA DE CLÍNICAS")
        print("=" * 35)
        print("1 - Gerenciar Clínicas")
        print("2 - Gerenciar Pacientes")
        print("3 - Gerenciar Profissionais")
        print("4 - Gerenciar Tipos de Atendimento")
        print("5 - Gerenciar Procedimentos")
        print("6 - Gerenciar Atendimentos")
        print("7 - Relatórios")
        print("0 - Encerrar Sistema")
        print("=" * 35)

        try:
            opcao = int(input("Escolha a opção: "))
            return opcao
        except ValueError:
            return -1

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")