
from datetime import time


class TelaClinica:
    def tela_opcoes(self) -> int:
        print("\n=== GERENCIAR CLÍNICAS ===")
        print("1 - Cadastrar Clínica")
        print("2 - Excluir Clínica")
        print("3 - Alterar Horário")
        print("4 - Listar Clínicas Abertas")
        print("5 - Listar Todas as Clínicas")
        print("6 - Alterar Nome")
        print("7 - Alterar Cidade")
        print("8 - Alterar Descrição")
        print("0 - Retornar")

        try:
            return int(input("Escolha a opção: "))
        except ValueError:
            return -1

    def pega_horario(self, campo: str) -> time:
        while True:
            try:
                texto = input(
                    f"{campo} (HH:MM): "
                ).strip()

                h, m = map(int, texto.split(":"))
                return time(h, m)

            except ValueError:
                print(
                    "[AVISO]: Horário inválido! Use HH:MM."
                )

    def pega_novos_horarios(self) -> dict:
        while True:
            abertura = self.pega_horario(
                "Horário de abertura"
            )
            fechamento = self.pega_horario(
                "Horário de fechamento"
            )

            if abertura < fechamento:
                return {
                    "abertura": abertura,
                    "fechamento": fechamento
                }

            print(
                "[AVISO]: O fechamento deve ser "
                "posterior à abertura!"
            )

    def pega_dados_clinica(self) -> dict:
        print("\n--- Dados da Clínica ---")

        dados = {
            "nome": input("Nome: ").strip(),
            "cidade": input("Cidade: ").strip(),
            "descricao": input("Descrição: ").strip()
        }

        dados.update(self.pega_novos_horarios())
        return dados

    def pega_novo_dado(self, campo: str) -> str:
        return input(f"Novo(a) {campo}: ").strip()

    def mostra_clinica(self, dados: dict) -> None:
        print(
            f"Nome: {dados['nome']} | "
            f"Cidade: {dados['cidade']} | "
            f"Descrição: {dados['descricao']} | "
            f"Funcionamento: "
            f"{dados['abertura']:%H:%M} às "
            f"{dados['fechamento']:%H:%M}"
        )

    def seleciona_clinica(self) -> str:
        return input("Nome da clínica: ").strip()

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")
