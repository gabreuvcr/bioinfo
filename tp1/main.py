from globais import BLOSUM_62, PENALIDADE_INDEL
import sys

class Celula:
    def __init__(self, valor=None, ponteiro=''):
        self.valor = valor
        self.ponteiro = ponteiro

def sequencia_arquivo(nome_arquivo):
    seq = ''
    try:
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                if not linha.startswith('>'):
                    seq += linha.replace('\n', '')
    except:
        print(f"Informe o nome do arquivo corretamente, {nome_arquivo} não encontrado.")
        exit()
    return seq

def trata_sequencias(arq1, arq2):
    v_seq, w_seq = sequencia_arquivo(arq1), sequencia_arquivo(arq2)
    v_seq, w_seq = v_seq.upper().strip(), w_seq.upper().strip()
    return v_seq, w_seq

def imprime(matriz, v_seq, w_seq):
    matriz_imp = []
    for i in range(LINHA + 1):
        line = []
        for j in range(COLUNA + 1):
            if (i == 0 and j == 0):
                line.append(' ')
            elif ((i == 1 and j == 0) or (i == 0 and j == 1)):
                line.append('*')
            elif (i == 0):
                line.append(v_seq[j - 2])
            elif (j == 0):
                line.append(w_seq[i - 2])
            else:
                line.append(matriz[i - 1][j - 1])
        matriz_imp.append(line)

    for i in range(LINHA + 1):
        for j in range(COLUNA + 1):
            if (type(matriz_imp[i][j]) == Celula):
                print(f"{str(matriz_imp[i][j].valor) + matriz_imp[i][j].ponteiro:<6}", end='')
            else:
                print(f"{matriz_imp[i][j]:<6}", end='')
        print()
    print()
    
def matriz_inicial():
    matriz = []
    for i in range(LINHA):
        line = []
        for j in range(COLUNA):
            if i == 0 or j == 0:
                line.append(Celula(0))
            else:
                line.append(Celula())
        matriz.append(line)
    return matriz

def valor_e_ponteiro(cima, lado, diagonal):
    if (diagonal >= cima and diagonal >= lado):
        return diagonal, "\\"
    elif (COLUNA >= LINHA):
        if (lado >= cima):
            return lado, "_"
        else:
            return cima, "|"
    elif (LINHA > COLUNA):
        if (cima >= lado):
            return cima, "|"
        else:
            return lado, "_"

def matriz_alinhamento(v_seq, w_seq):
    matriz = matriz_inicial()
    for i in range(1, LINHA):
        for j in range(1, COLUNA):
            cima = matriz[i-1][j].valor + PENALIDADE_INDEL
            lado = matriz[i][j-1].valor + PENALIDADE_INDEL
            if (w_seq[i-1], v_seq[j-1]) in BLOSUM_62:
                diagonal = matriz[i-1][j-1].valor + BLOSUM_62[w_seq[i-1], v_seq[j-1]]
            else:
                diagonal = matriz[i-1][j-1].valor + BLOSUM_62[v_seq[j-1], w_seq[i-1]]
            valor, ponteiro = valor_e_ponteiro(cima, lado, diagonal)
            matriz[i][j].valor, matriz[i][j].ponteiro = valor, ponteiro
    return matriz

def alinhamento(matriz, v_seq, w_seq):
    v_alin, w_alin = "", ""
    linha_atual, coluna_atual = LINHA - 1, COLUNA - 1
    celula_atual = matriz[linha_atual][coluna_atual]
    while (celula_atual.valor != 0):
        if (celula_atual.ponteiro == "\\"):
            v_alin = v_seq[coluna_atual - 1] + v_alin
            w_alin = w_seq[linha_atual -1] + w_alin
            linha_atual -= 1
            coluna_atual -= 1
        elif (celula_atual.ponteiro == "_"):
            v_alin = v_seq[coluna_atual - 1] + v_alin
            w_alin = "-" + w_alin
            coluna_atual -= 1
        elif (celula_atual.ponteiro == "|"):
            v_alin = "-" + v_alin
            w_alin = w_seq[linha_atual - 1] + w_alin
            linha_atual -= 1
        celula_atual = matriz[linha_atual][coluna_atual]
    return "-" + v_alin, "-" + w_alin

if len(sys.argv) < 3:
    print("Informe o nome dos dois arquivos.")
    print("> python main.py <arq1>.<ext> <arq2>.<ext> [-i]")
    exit()

imp = 0
if len(sys.argv) > 3 and sys.argv[3] == '-i':
    imp = 1

v_seq, w_seq = trata_sequencias(sys.argv[1], sys.argv[2])

LINHA, COLUNA = len(w_seq) + 1, len(v_seq) + 1

matriz = matriz_alinhamento(v_seq, w_seq)
v_alin, w_alin = alinhamento(matriz, v_seq, w_seq)

if (imp):
    imprime(matriz, v_seq, w_seq)
print(v_alin)
print(w_alin)
