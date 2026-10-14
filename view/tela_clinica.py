from datetime import time


class TelaClinica:
    def tela_opcoes(self) -> int:
        print("\n" + "=" * 35)
        print("        GERENCIAR CLÍNICAS")
        print("=" * 35)
        print("1 - Cadastrar Clínica")
        print("2 - Excluir Clínica")
        print("3 - Alterar Horário")
        print("4 - Listar Clínicas Abertas")
        print("0 - Retornar")
        print("=" * 35)

        try:
            return int(input("Escolha a opção: "))
        except ValueError:
            return -1

    def pega_dados_clinica(self) -> dict:
    print("\n--- Dados da Clínica ---")
    nome = input("Nome da clínica: ").strip()
    cidade = input("Cidade: ").strip()
    descricao = input("Descrição: ").strip()

    while True:
        try:
            abertura_str = input(
                "Horário de abertura (HH:MM): "
            ).strip()
            h_ab, m_ab = map(int, abertura_str.split(":"))
            abertura = time(h_ab, m_ab)
            break
        except ValueError:
            print("[AVISO]: Horário de abertura inválido!")

    while True:
        try:
            fechamento_str = input(
                "Horário de fechamento (HH:MM): "
            ).strip()
            h_fc, m_fc = map(int, fechamento_str.split(":"))
            fechamento = time(h_fc, m_fc)

            if fechamento <= abertura:
                print(
                    "[AVISO]: O fechamento deve ser "
                    "posterior à abertura!"
                )
                continue

            break
        except ValueError:
            print("[AVISO]: Horário de fechamento inválido!")

    return {
        "nome": nome,
        "cidade": cidade,
        "descricao": descricao,
        "abertura": abertura,
        "fechamento": fechamento
    }

    def mostra_clinica(self, dados: dict) -> None:
        abertura_str = dados['abertura'].strftime('%H:%M') if hasattr(dados['abertura'], 'strftime') else str(dados['abertura'])
        fechamento_str = dados['fechamento'].strftime('%H:%M') if hasattr(dados['fechamento'], 'strftime') else str(dados['fechamento'])
        print(f"Nome: {dados['nome']} | Abertura: {abertura_str} | Fechamento: {fechamento_str}")

    def seleciona_clinica(self) -> str:
        return input("Digite o nome da clínica: ").strip()

    def mostra_mensagem(self, msg: str) -> None:
        print(f"\n[AVISO]: {msg}")