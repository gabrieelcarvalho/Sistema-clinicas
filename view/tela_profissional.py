import re


def solicitar_cpf(campo: str = "CPF", opcional: bool = False) -> str:
    while True:
        cpf = input(f"{campo} (000.000.000-00): ").strip()

        if opcional and not cpf:
            return ""

        if re.fullmatch(r"[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}", cpf):
            return cpf

        print("[AVISO]: CPF inválido! Use 000.000.000-00.")


def solicitar_celular(campo: str = "Celular") -> str:
    while True:
        celular = input(f"{campo} ((00) 00000-0000): ").strip()

        if re.fullmatch(r"\([0-9]{2}\) [0-9]{5}-[0-9]{4}", celular):
            return celular

        print("[AVISO]: Celular inválido! Use (00) 00000-0000.")


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
            "cpf": solicitar_cpf(),
            "celular": solicitar_celular(),
            "especialidade": input("Especialidade: ").strip(),
            "registro_profissional": input(
                "Registro Profissional: "
            ).strip()
        }

    def pega_novo_dado(self, campo: str) -> str:
        if campo == "cpf":
            return solicitar_cpf("Novo CPF")

        if campo == "celular":
            return solicitar_celular("Novo celular")

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
        if tipo.upper() == "CPF":
            return solicitar_cpf("CPF do profissional")

        return input(
            f"Digite o {tipo} do profissional: "
        ).strip()

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")