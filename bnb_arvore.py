import math

from read import matriz               # reaproveita a matriz do read.py
from custo import custo_rota
from guloso import guloso
from guloso_arvore import pedir_numero


def formatar(rota):
    return " → ".join(str(c + 1) for c in rota + [rota[0]])


def bnb_arvore(matriz, usar_guloso=True):
    n = len(matriz)
    if usar_guloso:
        melhor_rota = guloso(matriz)              # limite inicial: a rota do guloso
        melhor_custo = custo_rota(melhor_rota, matriz)
        print(f"Limite inicial (guloso): {melhor_custo}   rota {formatar(melhor_rota)}")
    else:
        melhor_rota = None
        melhor_custo = math.inf                   # sem limite: a primeira rota completa vira a melhor
        print("Sem limite inicial")
    nos = 1                                       # a raiz (cidade 1) já conta, igual ao bnb.py
    podas = 0

    rota = [0]                                    # toda rota começa na cidade 1
    visitada = [False] * n
    visitada[0] = True
    print()
    print("1 (custo 0)")

    def explorar(custo, prefixo):
        nonlocal melhor_rota, melhor_custo, nos, podas
        atual = rota[-1]
        filhas = [c for c in range(n) if not visitada[c]]
        for i, c in enumerate(filhas):            # branch: cada cidade não visitada é um galho
            ultima = i == len(filhas) - 1
            novo = custo + matriz[atual][c]
            linha = f"{prefixo}{'└── ' if ultima else '├── '}{c + 1} ({novo})"
            nos += 1

            if novo >= melhor_custo:              # bound: já passou da melhor rota, corta o galho
                podas += 1
                print(f"{linha}  ← PODA ({novo} >= {melhor_custo})")
                continue

            rota.append(c)
            visitada[c] = True
            if len(rota) == n:                    # rota completa: soma a volta para o início
                total = novo + matriz[c][0]
                if total < melhor_custo:
                    melhor_custo = total
                    melhor_rota = rota[:]
                    print(f"{linha} → volta para 1: {total}  ← NOVA MELHOR")
                else:
                    print(f"{linha} → volta para 1: {total}  (não melhora)")
            else:
                print(linha)
                explorar(novo, prefixo + ("    " if ultima else "│   "))
            rota.pop()                            # backtracking: desfaz e tenta o próximo galho
            visitada[c] = False

    explorar(0, "")
    return melhor_rota, melhor_custo, nos, podas


if __name__ == "__main__":
    print()
    print("===== Branch and bound em árvore =====")
    k = pedir_numero("Quantas cidades usar (2 a 7)? ", 2, 7)
    usar_guloso = input("Usar o guloso como limite inicial? (s/n) ").strip().lower() == "s"

    sub = [linha[:k] for linha in matriz[:k]]     # só as k primeiras cidades
    print()
    rota, custo, nos, podas = bnb_arvore(sub, usar_guloso)
    print()
    print("Melhor rota:", formatar(rota))
    print("Custo:", custo)
    print(f"Nós visitados: {nos}   podas: {podas}")
    print(f"Sem poda seriam {math.factorial(k - 1)} rotas completas")
