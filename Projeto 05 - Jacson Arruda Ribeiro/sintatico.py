from gerador import GeradorCodigo

class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_atual = self.tokens[self.pos] if self.tokens else None
        self.gerador = GeradorCodigo()

    def avancar(self):
        self.pos += 1
        self.token_atual = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def match(self, tipo_esperado):
        if self.token_atual and self.token_atual['tipo'] == tipo_esperado:
            self.avancar()
        else:
            encontrado = self.token_atual['valor'] if self.token_atual else "Fim da expressão"
            raise SyntaxError(f"[Erro Sintático] Esperava '{tipo_esperado}', mas encontrou '{encontrado}'.")

    # Regra: E -> T E'
    def E(self):
        val_T, nome_T = self.T()
        return self.E_linha(val_T, nome_T)

    # Regra: E' -> + T E' | epsilon
    def E_linha(self, herdado_val, herdado_nome):
        if self.token_atual and self.token_atual['tipo'] == '+':
            self.match('+')
            val_T, nome_T = self.T()
            
            # Cálculo Semântico e Geração de Código
            novo_val = herdado_val + val_T
            temp = self.gerador.novo_temp()
            self.gerador.adicionar_instrucao(f"{temp} = {herdado_nome} + {nome_T}")
            
            return self.E_linha(novo_val, temp)
        return herdado_val, herdado_nome

    # Regra: T -> F T'
    def T(self):
        val_F, nome_F = self.F()
        return self.T_linha(val_F, nome_F)

    # Regra: T' -> * F T' | epsilon
    def T_linha(self, herdado_val, herdado_nome):
        if self.token_atual and self.token_atual['tipo'] == '*':
            self.match('*')
            val_F, nome_F = self.F()
            
            # Cálculo Semântico e Geração de Código
            novo_val = herdado_val * val_F
            temp = self.gerador.novo_temp()
            self.gerador.adicionar_instrucao(f"{temp} = {herdado_nome} * {nome_F}")
            
            return self.T_linha(novo_val, temp)
        return herdado_val, herdado_nome

    # Regra: F -> ( E ) | id
    def F(self):
        if self.token_atual and self.token_atual['tipo'] == 'id':
            val_real = int(self.token_atual['valor'])
            nome_str = self.token_atual['valor']
            self.match('id')
            return val_real, nome_str
        elif self.token_atual and self.token_atual['tipo'] == '(':
            self.match('(')
            val_real, nome_str = self.E()
            self.match(')')
            return val_real, nome_str
        else:
            encontrado = self.token_atual['valor'] if self.token_atual else "Fim"
            raise SyntaxError(f"[Erro Sintático] Esperava número ou '(', mas encontrou '{encontrado}'.")

    def parse(self):
        if not self.tokens:
            return None
        try:
            val_final, nome_final = self.E()
            if self.token_atual is not None:
                raise SyntaxError(f"[Erro Sintático] Símbolo inesperado no final: '{self.token_atual['valor']}'")
            return val_final
        except SyntaxError as e:
            print(e)
            return None
