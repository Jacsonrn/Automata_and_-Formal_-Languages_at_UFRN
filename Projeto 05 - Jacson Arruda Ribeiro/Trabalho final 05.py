import re

def analisador_lexico(expressao):
    tokens = []
    # A RegEx divide em grupos: 1(id), 2(+), 3(*), 4( ( ), 5( ) ), 6(Erro/Inválido)
    padrao = r'(\d+)|(\+)|(\*)|(\()|(\))|([^\s])'
    
    for match in re.finditer(padrao, expressao):
        if match.group(1):
            tokens.append({'tipo': 'id', 'valor': match.group(1)})
        elif match.group(2):
            tokens.append({'tipo': '+', 'valor': match.group(2)})
        elif match.group(3):
            tokens.append({'tipo': '*', 'valor': match.group(3)})
        elif match.group(4):
            tokens.append({'tipo': '(', 'valor': match.group(4)})
        elif match.group(5):
            tokens.append({'tipo': ')', 'valor': match.group(5)})
        elif match.group(6):
            # Capturou algo que não é espaço nem os símbolos permitidos
            print(f"[Erro Léxico] Caractere inválido encontrado: '{match.group(6)}'")
            return None 
            
    return tokens

def main():
    # Laço contínuo exigido pelo trabalho
    while True:
        expressao = input("\nDigite uma expressão aritmética (ou 'sair' para encerrar): ")
        
        if expressao.lower() == 'sair':
            break

        tokens = analisador_lexico(expressao)
        
        if tokens is not None:
            print("[OK] Análise Léxica sem erros!")
            print("Tokens extraídos:")
            for t in tokens:
                print(f"  [{t['tipo']}] -> {t['valor']}")
        else:
            print("-> Por favor, digite uma nova expressão.")

if __name__ == "__main__":
    main()