# Trabalho 04: Gramáticas Livres de Contexto (GLC)

Este repositório contém a solução para a 4ª Lista de Programação da disciplina **Autômatos e Linguagens Formais (DCA-3705)** da **Universidade Federal do Rio Grande do Norte (UFRN)**.

## Descrição do Projeto

O programa em C++ implementa um motor interativo para simular as regras de derivação de uma **Gramática Livre de Contexto**, definida formalmente pela quádrupla `G = <V, Σ, R, S>`, onde:
- **V**: Conjunto finito de variáveis (letras maiúsculas).
- **Σ**: Conjunto finito de terminais (letras minúsculas ou dígitos).
- **R**: Conjunto finito de regras de produção.
- **S**: Variável inicial (start).

O software permite que o usuário interaja passo a passo com a palavra sendo gerada, escolhendo quais regras de derivação habilitadas deseja aplicar até que a palavra contenha apenas símbolos terminais. A substituição prioriza a técnica de **derivação mais à esquerda** (*Leftmost Derivation*).

## Funcionalidades

1. **Configuração Flexível**:
   - Inserção de gramáticas manualmente via teclado.
   - Carregamento de gramáticas de teste pré-configuradas no código.
2. **Identificação Dinâmica de Regras**:
   - Em cada passo da derivação, o programa varre a cadeia de caracteres atual e filtra rigorosamente para mostrar ao usuário **apenas** as regras de produção aplicáveis às variáveis presentes naquele momento.
3. **Suporte à Transição Vazia (Épsilon)**:
   - Tratamento completo para regras que derivam em vazio (epsilon), representadas pelos símbolos `&` ou `#`.

## Exemplos Embutidos para Teste

O programa já conta com duas gramáticas embutidas para validação rápida (Passo 5 do escopo do projeto):
* **Gramática 1**: Reconhecedor de Palíndromos sobre o alfabeto {0, 1}.
* **Gramática 2**: Gera a linguagem de exemplo `G = <{A,B}, {0,1}, R, A>` usando as regras `A -> 0A1 | B` e `B -> #`.

## Como Compilar e Executar

Para compilar o código fonte, você precisará de um compilador C++ (como o `g++` no GCC ou MinGW).

1. Abra o terminal na pasta do projeto.
2. Compile o código com o seguinte comando:
   ```bash
   g++ "Trabalho 04.cpp" -o derivador_glc
   ```
3. Execute o programa gerado:
   - **No Windows:**
     ```cmd
     derivador_glc.exe
     ```
   - **No Linux/macOS:**
     ```bash
     ./derivador_glc
     ```

## Autor
* **Jacson Arruda Ribeiro** - Estudante de Engenharia de Computação / UFRN.