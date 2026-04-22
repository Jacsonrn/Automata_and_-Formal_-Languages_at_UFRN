import re

def aplicar_filtros_regex(caminho_entrada, caminho_saida):
    try:
        # Lê o conteúdo do arquivo .txt original
        with open(caminho_entrada, 'r', encoding='utf-8') as f:
            texto_original = f.read()

        if not texto_original.strip():
            print("O arquivo está vazio.")
            return

        print("Lendo e limpando o texto...")

        # 1. Remove qualquer conteúdo entre colchetes (ex: [suspiro], [música])
        texto_limpo = re.sub(r'\[.*?\]', '', texto_original)
        
        # 2. Remove aspas duplas e simples
        texto_limpo = texto_limpo.replace('"', '').replace("'", "")
        
        # 3. Normaliza os espaços (remove múltiplos espaços e quebras de linha excessivas)
        texto_limpo = " ".join(texto_limpo.split())
        
        # 4. Fatiamento (Chunking): Divide o texto em frases usando (. ! ?) seguidos de espaço
        frases = re.split(r'(?<=[.!?]) +', texto_limpo)

        frases_processadas = []

        for frase in frases:
            # 5. Remove símbolos estranhos (mantém letras, números, espaços, acentos, '?' e '!')
            frase_limpa = re.sub(r'[^\w\s\u00C0-\u00FF?!]', '', frase).strip()
            
            # Mantém a regra do seu código: pular strings menores que 2 caracteres
            if len(frase_limpa) >= 2:
                frases_processadas.append(frase_limpa)

        # Salva o texto processado no novo arquivo, colocando uma frase por linha
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            for frase in frases_processadas:
                f.write(frase + '\n')

        print(f"Sucesso! Arquivo limpo salvo em: {caminho_saida}")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_entrada}' não foi encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    arquivo_in = "roteiro.txt"
    arquivo_out = "roteiro_limpo.txt"
    
    aplicar_filtros_regex(arquivo_in, arquivo_out)