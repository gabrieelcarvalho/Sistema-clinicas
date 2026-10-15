class ValorInvalidoException(Exception):
    def __init__(self, valor: float = None):
        if valor is not None:
            super().__init__(f"Valor R$ {valor:.2f} inválido! O valor deve ser maior que zero.")
        else:
            super().__init__("Valor inválido! O valor deve ser maior que zero.")