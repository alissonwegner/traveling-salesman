import csv
import math
import statistics
import time

import matplotlib.pyplot as plt

from read import matriz               # reaproveita a matriz do read.py
from custo import custo_rota
from guloso import guloso
from bnb import branch_and_bound

OTIMO_BERLIN52 = 7542                 # ótimo conhecido do berlin52 inteiro (TSPLIB)
TAMANHOS_BNB = list(range(4, 14))     # 4 a 13 cidades: acima disso o B&B fica lento demais
TAMANHOS_GULOSO = list(range(4, 53))  # 4 a 52 cidades
REPETICOES_BNB = 5
REPETICOES_GULOSO = 30                # o guloso é rápido demais: mais repetições deixam a média estável


def sub_matriz(k):
    return [linha[:k] for linha in matriz[:k]]      # só as k primeiras cidades


def medir(funcao, repeticoes):
    tempos = []
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        resultado = funcao()
        tempos.append((time.perf_counter() - inicio) * 1000)   # em milissegundos
    return resultado, statistics.mean(tempos), statistics.stdev(tempos)


def grafico_tempo(tamanhos, medias, desvios, teoria, nome_teoria, titulo, arquivo, log=False):
    plt.figure(figsize=(8, 5))
    plt.errorbar(tamanhos, medias, yerr=desvios, fmt="o-", capsize=3, label="medido (média ± desvio padrão)")
    escala = medias[-1] / teoria(tamanhos[-1])      # encaixa a curva teórica no último ponto medido
    plt.plot(tamanhos, [escala * teoria(n) for n in tamanhos], "--", label=nome_teoria)
    if log:
        plt.yscale("log")                           # escala log: cada linha do eixo é 10x a anterior
    plt.xlabel("Número de cidades (n)")
    plt.ylabel("Tempo (ms)")
    plt.title(titulo)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(arquivo, dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    linhas = []                                     # cada item vira uma linha do resultados.csv
    otimos = {52: OTIMO_BERLIN52}                   # ótimo de cada tamanho (o B&B preenche de 4 a 13)

    # ---------- Branch and bound ----------
    print()
    print(f"===== Branch and bound ({REPETICOES_BNB} repetições por tamanho, leva ~1 min) =====")
    print(f"{'Cidades':>7}{'Custo':>8}{'Média (ms)':>14}{'Desvio (ms)':>13}{'Nós':>12}{'Podas':>12}")
    bnb_medias, bnb_desvios = [], []
    for k in TAMANHOS_BNB:
        sub = sub_matriz(k)
        (rota, custo, nos, podas), media, desvio = medir(lambda: branch_and_bound(sub), REPETICOES_BNB)
        otimos[k] = custo
        bnb_medias.append(media)
        bnb_desvios.append(desvio)
        print(f"{k:>7}{custo:>8}{media:>14.3f}{desvio:>13.3f}{nos:>12}{podas:>12}")
        linhas.append({"algoritmo": "B&B", "cidades": k, "custo": custo, "otimo": custo, "diferenca_pct": 0,
                       "tempo_medio_ms": round(media, 4), "desvio_ms": round(desvio, 4), "nos": nos, "podas": podas})

    # ---------- Guloso ----------
    print()
    print(f"===== Guloso ({REPETICOES_GULOSO} repetições por tamanho) =====")
    print(f"{'Cidades':>7}{'Custo':>8}{'Ótimo':>8}{'Diferença':>11}{'Média (ms)':>14}{'Desvio (ms)':>13}")
    gul_medias, gul_desvios, gul_diferencas = [], [], {}
    for k in TAMANHOS_GULOSO:
        sub = sub_matriz(k)
        rota, media, desvio = medir(lambda: guloso(sub), REPETICOES_GULOSO)
        custo = custo_rota(rota, sub)
        otimo = otimos.get(k)                       # None quando o ótimo não é conhecido (14 a 51)
        diferenca = (custo - otimo) / otimo * 100 if otimo else None
        if diferenca is not None:
            gul_diferencas[k] = diferenca
        gul_medias.append(media)
        gul_desvios.append(desvio)
        texto = f"{diferenca:.1f}%" if diferenca is not None else "—"
        print(f"{k:>7}{custo:>8}{otimo or '—':>8}{texto:>11}{media:>14.4f}{desvio:>13.4f}")
        linhas.append({"algoritmo": "Guloso", "cidades": k, "custo": custo, "otimo": otimo or "",
                       "diferenca_pct": "" if diferenca is None else round(diferenca, 2),
                       "tempo_medio_ms": round(media, 4), "desvio_ms": round(desvio, 4), "nos": "", "podas": ""})

    # ---------- Arquivos ----------
    with open("resultados.csv", "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=linhas[0].keys())
        escritor.writeheader()
        escritor.writerows(linhas)

    # lambda = função de uma linha: aqui, a fórmula da complexidade prevista na teoria
    grafico_tempo(TAMANHOS_BNB, bnb_medias, bnb_desvios, lambda n: math.factorial(n - 1), "teoria: (n − 1)!",
                  "Branch and bound: tempo × número de cidades", "tempo_bnb.png", log=True)
    grafico_tempo(TAMANHOS_GULOSO, gul_medias, gul_desvios, lambda n: n ** 2, "teoria: n²",
                  "Guloso: tempo × número de cidades", "tempo_guloso.png")

    plt.figure(figsize=(8, 5))
    barras = plt.bar([str(k) for k in gul_diferencas], list(gul_diferencas.values()), color="tab:red")
    plt.bar_label(barras, fmt="%.1f%%", fontsize=8)
    plt.xlabel("Número de cidades (n)")
    plt.ylabel("Diferença do ótimo (%)")
    plt.title("Guloso: quanto a rota ficou pior que a ótima")
    plt.grid(axis="y", alpha=0.3)
    plt.savefig("qualidade_guloso.png", dpi=150, bbox_inches="tight")
    plt.close()

    print()
    print("Arquivos gerados: resultados.csv, tempo_bnb.png, tempo_guloso.png, qualidade_guloso.png")
