class TelaProfissional:
    def tela_opcoes(self):
        print("\n" + "=" * 20 + " PROFISSIONAIS " + "=" * 20)
        print("1 - Cadastrar Profissional")
        print("2 - Alterar Nome")
        print("3 - Alterar CPF")
        print("4 - Alterar Registro")
        print("5 - Alterar Especialidade")
        print("6 - Listar Profissionais")
        print("7 - Excluir Profissional")
        print("0 - Retornar")

        while True:
            try:
                opcao = int(input("Escolha a opção: "))
                if 0 <= opcao <= 7:
                    return opcao
                print("Opção inválida! Escolha entre 0 e 7.")
            except ValueError:
                print("Entrada inválida! Digite apenas números inteiros.")

    def pega_dados_profissional(self):
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

    def mostra_profissional(self, dados: dict):
        print(
            f"Nome: {dados['nome']} | CPF: {dados['cpf']} | "
            f"Celular: {dados['celular']} | Especialidade: {dados['especialidade']} | "
            f"Registro: {dados['registro_profissional']}"
        )

    def seleciona_profissional(self):
        return input("Digite o identificador do profissional (CPF ou Registro): ").strip()

    def mostra_mensagem(self, msg: str):
        print(f"\n[SISTEMA]: {msg}")