class TipoAtendimentoNaoCadastradoException(Exception):
    def __init__(self, codigo: int):
        self.mensagem = f"O tipo de atendimento com código '{codigo}' não está cadastrado no sistema!"
        super().__init__(self.mensagem)