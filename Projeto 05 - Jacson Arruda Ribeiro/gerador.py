class GeradorCodigo:
    def __init__(self):
        self.contador_temp = 1
        self.instrucoes = []

    def novo_temp(self):
        nome = f"t{self.contador_temp}"
        self.contador_temp += 1
        return nome

    def adicionar_instrucao(self, instrucao):
        self.instrucoes.append(instrucao)
