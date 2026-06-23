import re

class AnalisadorLexico:
    @staticmethod
    def analisar(expressao):
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
