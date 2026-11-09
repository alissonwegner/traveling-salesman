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


# ---------- Visual dos gráficos ----------
AZUL = "#2a78d6"          # o que foi medido
LARANJA = "#eb6834"       # o que a teoria prevê
TEXTO = "#2b2b29"
TEXTO_FRACO = "#6b6a65"

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.titlepad": 14,
    "axes.titlecolor": TEXTO, "axes.labelcolor": TEXTO_FRACO, "axes.labelpad": 8,
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#c9c8c2",
    "axes.grid": True, "axes.grid.axis": "y", "axes.axisbelow": True,
    "grid.color": "#ebeae5", "grid.linewidth": 1, "grid.linestyle": "-",
    "xtick.color": TEXTO_FRACO, "ytick.color": TEXTO_FRACO, "xtick.major.size": 0, "ytick.major.size": 0,
    "ytick.minor.size": 0, "xtick.major.pad": 6, "ytick.major.pad": 6,
    "legend.frameon": False, "legend.fontsize": 10, "legend.labelcolor": TEXTO,
    "figure.facecolor": "white", "savefig.dpi": 200,
})


def virgula(numero):
    return f"{numero:g}".replace(".", ",")            # 0.5 -> "0,5" (decimal em português)


def tempo_legivel(ms, _=None):
    # 0,001 ms vira "1 µs" e 1000 ms vira "1 s": fica mais fácil ler o eixo em escala log
    if ms >= 1000:
        return virgula(ms / 1000) + " s"
    if ms >= 1:
        return virgula(ms) + " ms"
    return virgula(round(ms * 1000, 6)) + " µs"


def grafico_tempo(tamanhos, medias, desvios, repeticoes, teoria, nome_teoria, titulo, arquivo, log=False):
    fig, eixo = plt.subplots(figsize=(8, 4.8))
    escala = medias[-1] / teoria(tamanhos[-1])      # encaixa a curva teórica no último ponto medido
    eixo.plot(tamanhos, [escala * teoria(n) for n in tamanhos], "--", color=LARANJA, lw=2, label=nome_teoria, zorder=3)
    muitos = len(tamanhos) > 15                     # com muitos pontos, só as bolinhas (sem linha ligando)
    eixo.errorbar(tamanhos, medias, yerr=desvios, color=AZUL, lw=0 if muitos else 2, marker="o",
                  ms=5 if muitos else 7, mec="white", mew=1 if muitos else 1.5, elinewidth=1, capsize=0,
                  ecolor="#9ec5f4", label=f"medido (média de {repeticoes} execuções)", zorder=2)
    if log:
        eixo.set_yscale("log")                      # escala log: cada linha do eixo é 10x a anterior
        eixo.yaxis.set_major_formatter(tempo_legivel)
        eixo.yaxis.set_minor_locator(plt.NullLocator())
        eixo.set_ylabel("Tempo (escala logarítmica)")
    else:
        eixo.yaxis.set_major_formatter(lambda y, _: virgula(round(y, 6)))
        eixo.set_ylim(bottom=0)
        eixo.set_ylabel("Tempo (ms)")
    eixo.set_xlabel("Número de pontos (n)")
    eixo.set_title(titulo)
    eixo.legend(loc="upper left")
    fig.savefig(arquivo, bbox_inches="tight")
    plt.close(fig)


def grafico_qualidade(diferencas, arquivo):
    # diferencas: {tamanho: % acima do ótimo}. De 14 a 51 o ótimo não é conhecido, então deixamos um espaço vazio
    tamanhos = sorted(diferencas)
    posicoes = [i if k <= 13 else i + 1.4 for i, k in enumerate(tamanhos)]   # deixa um espaço antes do 52
    vazio = (posicoes[-2] + posicoes[-1]) / 2
    fig, eixo = plt.subplots(figsize=(8, 4.8))
    barras = eixo.bar(posicoes, [diferencas[k] for k in tamanhos], width=0.6, color=AZUL)
    eixo.bar_label(barras, labels=[f"{diferencas[k]:.1f}%".replace(".", ",") for k in tamanhos],
                   padding=4, fontsize=9, color=TEXTO)
    eixo.text(vazio, 0.6, "14 a 51:\nsem rota\nótima\nconhecida", ha="center", fontsize=8.5, color=TEXTO_FRACO)
    eixo.set_xticks(posicoes, [str(k) for k in tamanhos])
    eixo.yaxis.set_major_formatter(lambda y, _: virgula(y) + "%")
    eixo.set_ylim(0, max(diferencas.values()) * 1.15)       # espaço para o rótulo da barra mais alta
    eixo.set_xlabel("Número de pontos (n)")
    eixo.set_ylabel("Rota do guloso acima da ótima")
    eixo.set_title("Quanto a rota do guloso ficou mais longa que a ótima")
    fig.savefig(arquivo, bbox_inches="tight")
    plt.close(fig)


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
    grafico_tempo(TAMANHOS_BNB, bnb_medias, bnb_desvios, REPETICOES_BNB, lambda n: math.factorial(n - 1),
                  "previsto pela teoria: (n − 1)!", "Tempo do branch and bound", "tempo_bnb.png", log=True)
    grafico_tempo(TAMANHOS_GULOSO, gul_medias, gul_desvios, REPETICOES_GULOSO, lambda n: n ** 2,
                  "previsto pela teoria: n²", "Tempo do guloso", "tempo_guloso.png")

    grafico_qualidade(gul_diferencas, "qualidade_guloso.png")

    print()
    print("Arquivos gerados: resultados.csv, tempo_bnb.png, tempo_guloso.png, qualidade_guloso.png")
