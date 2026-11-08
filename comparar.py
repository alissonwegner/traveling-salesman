import time

import matplotlib.pyplot as plt

from read import cidades, matriz      # reaproveita a leitura e a matriz do read.py
from custo import custo_rota
from guloso import guloso
from bnb import branch_and_bound
from bnb_arvore import formatar
from guloso_arvore import pedir_numero


def girar(rota, inicio):
    i = rota.index(inicio)                        # a rota é um ciclo: só muda a cidade por onde começa
    return rota[i:] + rota[:i]                    # o custo continua o mesmo


def comparar(matriz, inicio=0):
    t = time.perf_counter()
    rota = guloso(matriz, inicio)
    tempo = time.perf_counter() - t
    g = {"rota": rota, "custo": custo_rota(rota, matriz), "tempo": tempo}   # custo_rota já soma a volta

    t = time.perf_counter()
    rota, custo, nos, podas = branch_and_bound(matriz)
    tempo = time.perf_counter() - t
    b = {"rota": girar(rota, inicio), "custo": custo, "tempo": tempo, "nos": nos, "podas": podas}

    return g, b


def desenhar_lado_a_lado(pontos, g, b, inicio, arquivo="comparar.png"):
    fig, eixos = plt.subplots(1, 2, figsize=(14, 6))
    lados = [(eixos[0], "Guloso", g, "tab:red"), (eixos[1], "Branch and bound", b, "tab:green")]
    for eixo, nome, res, cor in lados:
        caminho = res["rota"] + [res["rota"][0]]  # ida e volta: fecha o ciclo no início
        eixo.plot([pontos[i][0] for i in caminho], [pontos[i][1] for i in caminho], color=cor, linewidth=1.5, zorder=1)
        eixo.scatter([p[0] for p in pontos], [p[1] for p in pontos], color="tab:blue", s=30, zorder=2)
        eixo.scatter(pontos[inicio][0], pontos[inicio][1], color="black", marker="*", s=200, zorder=3)  # início
        for i, (x, y) in enumerate(pontos):
            eixo.text(x + 12, y + 12, str(i + 1), fontsize=8)
        eixo.set_title(f"{nome} - custo {res['custo']}")
        eixo.set_aspect("equal")
    plt.savefig(arquivo, dpi=150, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    print()
    print("===== Comparação: guloso x branch and bound =====")
    k = pedir_numero("Quantas cidades usar (2 a 13; acima de 11 demora)? ", 2, 13)
    inicio = pedir_numero(f"Começar em qual cidade (1 a {k})? ", 1, k) - 1

    sub = [linha[:k] for linha in matriz[:k]]     # só as k primeiras cidades
    g, b = comparar(sub, inicio)

    print()
    print("Guloso:          ", formatar(g["rota"]))
    print("Branch and bound:", formatar(b["rota"]))
    print()
    print(f"{'Algoritmo':<18}{'Custo':>8}{'Tempo (ms)':>14}")
    print(f"{'Guloso':<18}{g['custo']:>8}{g['tempo'] * 1000:>14.3f}")
    print(f"{'Branch and bound':<18}{b['custo']:>8}{b['tempo'] * 1000:>14.3f}")
    print(f"B&B: {b['nos']} nós visitados, {b['podas']} podas")
    print()

    extra = g["custo"] - b["custo"]
    if extra == 0:
        print("O guloso achou a melhor rota.")
    else:
        print(f"O guloso ficou {extra} mais caro ({extra / b['custo'] * 100:.1f}% acima do ótimo).")
    print(f"O B&B levou {b['tempo'] / g['tempo']:.0f}x o tempo do guloso.")

    desenhar_lado_a_lado(cidades[:k], g, b, inicio)
