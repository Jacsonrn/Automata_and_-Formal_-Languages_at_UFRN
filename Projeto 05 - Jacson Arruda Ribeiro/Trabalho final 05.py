import re

# --- FASE 1: Analisador Léxico ---
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

# --- FASES 2, 3 e 4: Analisador Sintático, Semântico (Cálculo) e Geração de Código ---
class CompiladorCompleto:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_atual = self.tokens[self.pos] if self.tokens else None
        self.contador_temp = 1
        self.instrucoes = []

    def avancar(self):
        self.pos += 1
        self.token_atual = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def match(self, tipo_esperado):
        if self.token_atual and self.token_atual['tipo'] == tipo_esperado:
            self.avancar()
        else:
            encontrado = self.token_atual['valor'] if self.token_atual else "Fim da expressão"
            raise SyntaxError(f"[Erro Sintático] Esperava '{tipo_esperado}', mas encontrou '{encontrado}'.")

    def novo_temp(self):
        nome = f"t{self.contador_temp}"
        self.contador_temp += 1
        return nome

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
            temp = self.novo_temp()
            self.instrucoes.append(f"{temp} = {herdado_nome} + {nome_T}")
            
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
            temp = self.novo_temp()
            self.instrucoes.append(f"{temp} = {herdado_nome} * {nome_F}")
            
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
            print(e) # Exibe o erro sem quebrar o laço
            return None

# --- Integração Final (Laço Contínuo) ---
def main():
    print("=== TRADUTOR DE EXPRESSÕES ARITMÉTICAS ===")
    while True:
        expressao = input("\nDigite uma expressão (ou 'sair'): ")
        if expressao.lower() == 'sair':
            break

        tokens = analisador_lexico(expressao)
        
        if tokens is not None: 
            compilador = CompiladorCompleto(tokens)
            resultado_matematico = compilador.parse()
            
            if resultado_matematico is not None:
                print(f"[OK] Análise Léxica e Sintática passaram!")
                print(f"-> Resultado Matemático: {resultado_matematico}")
                print("-> Código de Três Endereços:")
                for inst in compilador.instrucoes:
                    print(f"   {inst}")

if __name__ == "__main__":
     main()