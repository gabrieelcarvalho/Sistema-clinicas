class ClinicaNaoCadastradaException(Exception):
    def __init__(self, nome: str):
        self.mensagem = f"A clínica '{nome}' não está cadastrada no sistema!"
        super().__init__(self.mensagem)