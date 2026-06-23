from lexico import AnalisadorLexico
from sintatico import AnalisadorSintatico

def main():
    print("=== TRADUTOR DE EXPRESSÕES ARITMÉTICAS ===")
    while True:
        try:
            expressao = input("\nDigite uma expressão (ou 'sair'): ")
        except EOFError:
            break

        if expressao.lower() == 'sair':
            break

        tokens = AnalisadorLexico.analisar(expressao)
        
        if tokens is not None: 
            analisador = AnalisadorSintatico(tokens)
            resultado_matematico = analisador.parse()
            
            if resultado_matematico is not None:
                print(f"[OK] Análise Léxica e Sintática passaram!")
                print(f"-> Resultado Matemático: {resultado_matematico}")
                print("-> Código de Três Endereços:")
                for inst in analisador.gerador.instrucoes:
                    print(f"   {inst}")

if __name__ == "__main__":
     main()
