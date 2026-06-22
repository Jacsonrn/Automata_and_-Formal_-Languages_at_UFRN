import re

# --- DIA 1: Analisador Léxico ---
def analisador_lexico(expressao):
    tokens = []
    padrao = r'(\d+)|(\+)|(\*)|(\()|(\))|([^\s])'
    for match in re.finditer(padrao, expressao):
        if match.group(1): tokens.append({'tipo': 'id', 'valor': match.group(1)})
        elif match.group(2): tokens.append({'tipo': '+', 'valor': match.group(2)})
        elif match.group(3): tokens.append({'tipo': '*', 'valor': match.group(3)})
        elif match.group(4): tokens.append({'tipo': '(', 'valor': match.group(4)})
        elif match.group(5): tokens.append({'tipo': ')', 'valor': match.group(5)})
        elif match.group(6):
            print(f"[Erro Léxico] Caractere inválido: '{match.group(6)}'")
            return None 
    return tokens

# --- DIA 2 e 3: Analisador Sintático e Semântico ---
class AnalisadorSintaticoSemantico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_atual = self.tokens[self.pos] if self.tokens else None

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
        val_T = self.T()
        return self.E_linha(val_T)

    # Regra: E' -> + T E' | epsilon
    def E_linha(self, herdado): # Parâmetro herdado adicionado
        if self.token_atual and self.token_atual['tipo'] == '+':
            self.match('+')
            val_T = self.T()
            # Avaliação Semântica (Soma)
            novo_valor = herdado + val_T
            return self.E_linha(novo_valor)
        return herdado # epsilon: retorna o que já calculou

    # Regra: T -> F T'
    def T(self):
        val_F = self.F()
        return self.T_linha(val_F)

    # Regra: T' -> * F T' | epsilon
    def T_linha(self, herdado): # Parâmetro herdado adicionado
        if self.token_atual and self.token_atual['tipo'] == '*':
            self.match('*')
            val_F = self.F()
            # Avaliação Semântica (Multiplicação)
            novo_valor = herdado * val_F
            return self.T_linha(novo_valor)
        return herdado # epsilon: retorna o que já calculou

    # Regra: F -> ( E ) | id
    def F(self):
        if self.token_atual and self.token_atual['tipo'] == 'id':
            val = int(self.token_atual['valor']) # Extrai o valor real
            self.match('id')
            return val
        elif self.token_atual and self.token_atual['tipo'] == '(':
            self.match('(')
            val = self.E()
            self.match(')')
            return val
        else:
            encontrado = self.token_atual['valor'] if self.token_atual else "Fim"
            raise SyntaxError(f"[Erro Sintático] Esperava número ou '(', mas encontrou '{encontrado}'.")

    def parse(self):
        if not self.tokens:
            return None
        try:
            resultado = self.E()
            if self.token_atual is not None:
                raise SyntaxError(f"[Erro Sintático] Símbolo inesperado no final: '{self.token_atual['valor']}'")
            return resultado
        except SyntaxError as e:
            print(e)
            return None

# --- Estrutura Principal ---
def main():
    while True:
        expressao = input("\nDigite uma expressão aritmética (ou 'sair'): ")
        if expressao.lower() == 'sair':
            break

        tokens = analisador_lexico(expressao)
        
        if tokens is not None: 
            parser = AnalisadorSintaticoSemantico(tokens)
            resultado = parser.parse()
            
            if resultado is not None:
                print(f"[OK] Expressão válida! O resultado da conta é: {resultado}") # Exibe resultado [4]

if __name__ == "__main__":
    main()