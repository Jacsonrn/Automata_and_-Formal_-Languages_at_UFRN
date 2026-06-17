#include <iostream>
#include <vector>
#include <string>
#include <set>
#include <cctype>

using namespace std;

// Estrutura para armazenar as regras de producao (R)
struct Regra {
    int id;
    char origem;
    string destino; // Uma string vazia "" representara a transicao vazia (epsilon)
};

// Classe que representa a Gramatica Livre de Contexto (G = <V, Sigma, R, S>)
class GramaticaLivreContexto {
private:
    set<char> V;         // Conjunto finito de variaveis
    set<char> Sigma;     // Conjunto finito de terminais
    vector<Regra> R;     // Conjunto finito de regras de producao
    char S;              // Variavel inicial

public:
    GramaticaLivreContexto() : S(' ') {}

    // Valida se o caractere eh uma Variavel (Letra Maiuscula)
    bool isVariavel(char c) { return isupper(c); }

    // Valida se o caractere eh um Terminal (Letra minuscula ou digito)
    bool isTerminal(char c) { return islower(c) || isdigit(c); }

    void adicionarVariavel(char c) {
        if (isVariavel(c)) V.insert(c);
    }

    void adicionarTerminal(char c) {
        if (isTerminal(c)) Sigma.insert(c);
    }

    void definirStart(char c) {
        if (isVariavel(c)) {
            S = c;
            adicionarVariavel(c);
        } else {
            cout << "[Erro] A variavel inicial deve ser uma letra maiuscula.\n";
        }
    }

    void adicionarRegra(char origem, string destino) {
        if (!isVariavel(origem)) {
            cout << "[Erro] A origem '" << origem << "' deve ser uma variavel maiuscula.\n";
            return;
        }
        
        // Adiciona a regra numerada sequencialmente
        R.push_back({(int)R.size() + 1, origem, destino});
        
        // Povoa os conjuntos V e Sigma automaticamente lendo os caracteres
        adicionarVariavel(origem);
        for (char c : destino) {
            if (isVariavel(c)) adicionarVariavel(c);
            else if (isTerminal(c)) adicionarTerminal(c);
        }
    }

    // Metodo para verificar se o carregamento ocorreu corretamente
    void exibirGramatica() {
        cout << "\n=== Estado da Gramatica G = <V, Sigma, R, S> ===\n";
        
        cout << "V (Variaveis) : { ";
        for (char c : V) cout << c << " ";
        cout << "}\n";
        
        cout << "Sigma (Terminais): { ";
        for (char c : Sigma) cout << c << " ";
        cout << "}\n";
        
        cout << "S (Variavel Inicial): " << S << "\n";
        
        cout << "R (Regras de Producao):\n";
        for (const auto& regra : R) {
            cout << "  (" << regra.id << ") " << regra.origem << " -> " 
                 << (regra.destino.empty() ? "# (epsilon)" : regra.destino) << "\n";
        }
        cout << "================================================\n\n";
    }

    // Fase de execucao (derivacao)
    void derivar() {
        if (S == ' ') {
            cout << "[Erro] A gramatica nao possui variavel inicial definida.\n";
            return;
        }

        string derivacao = string(1, S); // O estado inicial contem apenas a variavel S
        cout << "=== FASE DE DERIVACAO ===\n";

        while (true) {
            cout << "\nEstado atual da palavra: " << (derivacao.empty() ? "# (epsilon)" : derivacao) << "\n";

            // Identificacao de Regras Ativas
            set<char> variaveisNaCadeia;
            for (char c : derivacao) {
                if (isVariavel(c)) {
                    variaveisNaCadeia.insert(c);
                }
            }
            
            vector<Regra> regrasAtivas;
            for (const auto& regra : R) {
                if (variaveisNaCadeia.count(regra.origem)) {
                    regrasAtivas.push_back(regra);
                }
            }

            if (regrasAtivas.empty()) {
                cout << "-> Nao ha mais regras habilitadas.\n";
                cout << "-> Palavra final gerada: " << (derivacao.empty() ? "# (epsilon)" : derivacao) << "\n";
                cout << "=== FIM DA DERIVACAO ===\n";
                break; 
            }

            cout << "Regras habilitadas (ativas):\n";
            for (const auto& regra : regrasAtivas) {
                cout << "  [" << regra.id << "] " << regra.origem << " -> " 
                     << (regra.destino.empty() ? "# (epsilon)" : regra.destino) << "\n";
            }

            int escolha;
            cout << "Selecione a regra pelo seu numero: ";
            cin >> escolha;

            bool aplicou = false;
            for (const auto& regra : regrasAtivas) {
                if (regra.id == escolha) {
                    size_t pos = derivacao.find(regra.origem);
                    derivacao.replace(pos, 1, regra.destino); 
                    cout << "-> [Acao] Regra " << regra.id << " aplicada com sucesso!\n";
                    aplicou = true;
                    break;
                }
            }
            if (!aplicou) cout << "[Erro] Numero invalido ou regra inativa. Tente novamente.\n";
        }
    }
};

void iniciarConfiguracao() {
    GramaticaLivreContexto G;3
    int opcao;
    
    do {
        cout << "--- PASSO 1: CONFIGURACAO DA GRAMATICA (DCA-3705) ---\n";
        cout << "1. Inserir gramatica manualmente via teclado\n";
        cout << "2. Carregar Gramatica 1: Reconhecedor de Palindromos (Codigo)\n";
        cout << "3. Carregar Gramatica 2: Exemplo G = <{A,B}, {0,1}, R, A> (Codigo)\n";
        cout << "0. Sair / Avancar para proxima etapa\n";
        cout << "Escolha uma opcao: ";
        cin >> opcao;
        
        if (opcao == 1) {
            G = GramaticaLivreContexto();
            char start;
            cout << "Digite a variavel inicial S (letra maiuscula): ";
            cin >> start;
            G.definirStart(start);
            
            int qtdRegras;
            cout << "Quantas regras deseja cadastrar? ";
            cin >> qtdRegras;
            
            for (int i = 0; i < qtdRegras; i++) {
                char origem;
                string destino;
                cout << "Regra [" << i + 1 << "] Origem (1 char): ";
                cin >> origem;
                cout << "Regra [" << i + 1 << "] Destino (digite '#' ou '&' para epsilon): ";
                cin >> destino;
                
                if (destino == "&" || destino == "#") destino = ""; // Trata entrada para Epsilon
                G.adicionarRegra(origem, destino);
            }
            G.exibirGramatica();
            G.derivar();
        } 
        else if (opcao == 2) {
            G = GramaticaLivreContexto();
            G.definirStart('P');
            G.adicionarRegra('P', "0P0");
            G.adicionarRegra('P', "1P1");
            G.adicionarRegra('P', "0");
            G.adicionarRegra('P', "1");
            G.adicionarRegra('P', ""); // Epsilon
            cout << "\n[OK] Gramatica de Palindromos carregada com sucesso!\n";
            G.exibirGramatica();
            G.derivar();
        }
        else if (opcao == 3) {
            G = GramaticaLivreContexto();
            G.definirStart('A');
            G.adicionarRegra('A', "0A1");
            G.adicionarRegra('A', "B");
            G.adicionarRegra('B', ""); // Epsilon
            cout << "\n[OK] Gramatica de Exemplo (A,B) carregada com sucesso!\n";
            G.exibirGramatica();
            G.derivar();
        }
    } while (opcao != 0);
    
    cout << "\n[Fim do Passo 1] Estruturas criadas. Pronto para a etapa de derivacao!\n";
}

int main() {
    iniciarConfiguracao();
    return 0;
}