#include <iostream>
#include <string>
#include <vector>
#include <cctype>

using namespace std;

// Estrutura do Dicionário (Desafio do Professor)
struct Dicionario {
    vector<string> unid = {"", "um", "dois", "tres", "quatro", "cinco", "seis", "sete", "oito", "nove"};
    vector<string> dez10 = {"dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"};
    vector<string> dez = {"", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"};
    vector<string> cent = {"", "cem", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos", "setecentos", "oitocentos", "novecentos"};
    string mil = "mil";
    string zero = "zero";
    string conector = " e ";
};

struct DicionarioEN {
    vector<string> unid = {"", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
    vector<string> dez10 = {"ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"};
    vector<string> dez = {"", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"};
    vector<string> cent = {"", "one hundred", "two hundred", "three hundred", "four hundred", "five hundred", "six hundred", "seven hundred", "eight hundred", "nine hundred"};
    string mil = "thousand";
    string zero = "zero";
    string conector = " ";
};

class ConversorMealy {
private:
    int idioma; // 1 = PT, 2 = EN

    // Máquina que processa blocos de 3 dígitos (Centena -> Dezena -> Unidade)
    string processarBloco(int num, bool isMilhar) {
        string saida = "";
        int c = num / 100;
        int d = (num % 100) / 10;
        int u = num % 10;

        // Seleção do Dicionário
        vector<string> v_unid, v_dez10, v_dez, v_cent;
        string conector;
        if (idioma == 1) {
            Dicionario pt; v_unid = pt.unid; v_dez10 = pt.dez10; v_dez = pt.dez; v_cent = pt.cent; conector = pt.conector;
            if (c == 1 && (d > 0 || u > 0)) v_cent[1] = "cento"; // Exceção do "cem" em PT
        } else {
            DicionarioEN en; v_unid = en.unid; v_dez10 = en.dez10; v_dez = en.dez; v_cent = en.cent; conector = en.conector;
        }

        // Transições Mealy (Saída gerada ao analisar a entrada)
        if (c > 0) {
            saida += v_cent[c];
            if ((d > 0 || u > 0) && idioma == 1) saida += conector;
            else if ((d > 0 || u > 0) && idioma == 2) saida += " and ";
        }

        if (d == 1) {
            saida += v_dez10[u]; // Exceção 10-19
        } else {
            if (d > 1) {
                saida += v_dez[d];
                if (u > 0) saida += conector;
            }
            if (u > 0) {
                // Trata o "um mil" em PT (geralmente dizemos apenas "mil")
                if (isMilhar && num == 1 && idioma == 1) saida += "";
                else saida += v_unid[u];
            }
        }
        return saida;
    }

public:
    ConversorMealy(int lang) : idioma(lang) {}

    void setIdioma(int lang) { idioma = lang; }

    // Chamada em Cascata
    void converter(int numero) {
        if (numero == 0) {
            cout << "-> Saida: " << (idioma == 1 ? "zero" : "zero") << "." << endl;
            return;
        }

        int milhares = numero / 1000;
        int unidades = numero % 1000;
        string resultado = "";

        if (milhares > 0) {
            resultado += processarBloco(milhares, true) + " " + (idioma == 1 ? "mil" : "thousand");
            if (unidades > 0) {
                if (unidades <= 100 || unidades % 100 == 0) resultado += (idioma == 1 ? " e " : " ");
                else resultado += (idioma == 1 ? " " : " ");
            }
        }
        
        if (unidades > 0) {
            resultado += processarBloco(unidades, false);
        }

        cout << "-> Saida: " << resultado << "." << endl;
    }
};

// Validador de Entrada (Trata "casa" e "-215")
bool isNumeroValido(string str) {
    for (char c : str) {
        if (!isdigit(c)) return false;
    }
    return true;
}

int main() {
    int idioma = 1;
    ConversorMealy maquina(idioma);
    string entrada;

    cout << "=== Maquina de Mealy: Numeros por Extenso ===" << endl;
    cout << "Digite 'm' para trocar o idioma (Atual: PT) ou 'q' para sair." << endl;

    while (true) {
        cout << "\nEntrada: ";
        cin >> entrada;

        if (entrada == "q") break;
        if (entrada == "m") {
            idioma = (idioma == 1) ? 2 : 1;
            maquina.setIdioma(idioma);
            cout << "-> Idioma alterado para: " << (idioma == 1 ? "Portugues" : "English") << endl;
            continue;
        }

        if (!isNumeroValido(entrada)) {
            cout << "-> Saida: entrada invalida (so respondo se a entrada for um numero entre 0 e 999.999)." << endl;
            continue;
        }

        try {
            int numero = stoi(entrada);
            if (numero >= 0 && numero <= 999999) {
                maquina.converter(numero);
            } else {
                cout << "-> Saida: entrada invalida (so respondo se a entrada for um numero entre 0 e 999.999)." << endl;
            }
        } catch (...) {
            cout << "-> Saida: entrada invalida (so respondo se a entrada for um numero entre 0 e 999.999)." << endl;
        }
    }

    return 0;
}