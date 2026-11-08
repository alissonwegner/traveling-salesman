import time

from read import cidades, matriz      # reaproveita a leitura e a matriz do read.py
from custo import custo_rota
from guloso import guloso
from guloso_arvore import pedir_numero
from mapa import desenhar


def branch_and_bound(matriz):
    n = len(matriz)
    melhor_rota = guloso(matriz)                  # limite inicial: a rota do guloso
    melhor_custo = custo_rota(melhor_rota, matriz)
    nos = 0                                       # quantos nós da árvore foram visitados
    podas = 0                                     # quantos galhos foram cortados

    rota = [0]                                    # toda rota começa na cidade 1
    visitada = [False] * n
    visitada[0] = True

    def explorar(custo):
        nonlocal melhor_rota, melhor_custo, nos, podas
        nos += 1
        if custo >= melhor_custo:                 # bound: já passou da melhor rota, corta o galho
            podas += 1
            return
        if len(rota) == n:                        # rota completa: soma a volta para o início
            total = custo + matriz[rota[-1]][0]
            if total < melhor_custo:
                melhor_custo = total
                melhor_rota = rota[:]
            return
        atual = rota[-1]
        for c in range(n):                        # branch: tenta cada cidade não visitada
            if not visitada[c]:
                rota.append(c)
                visitada[c] = True
                explorar(custo + matriz[atual][c])
                rota.pop()                        # backtracking: desfaz e tenta a próxima
                visitada[c] = False

    explorar(0)
    return melhor_rota, melhor_custo, nos, podas


if __name__ == "__main__":
    print()
    print("===== Branch and bound =====")
    k = pedir_numero("Quantas cidades usar (2 a 52; acima de 12 pode demorar)? ", 2, 52)

    sub = [linha[:k] for linha in matriz[:k]]     # só as k primeiras cidades
    inicio = time.perf_counter()
    rota, custo, nos, podas = branch_and_bound(sub)
    tempo = time.perf_counter() - inicio

    print("Melhor rota:", " → ".join(str(c + 1) for c in rota + [rota[0]]))
    print("Custo:", custo)
    print(f"Nós visitados: {nos}   podas: {podas}")
    print(f"Tempo: {tempo:.3f} s")
    desenhar(cidades[:k], rota=rota, titulo=f"Branch and bound ({k} cidades) - custo {custo}", arquivo="bnb.png")
