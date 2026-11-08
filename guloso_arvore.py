from read import matriz               # reaproveita a matriz do read.py
from custo import custo_rota


def guloso_arvore(matriz, inicio=0):
    n = len(matriz)
    rota = [inicio]
    visitada = [False] * n
    visitada[inicio] = True

    print(f"{inicio + 1} (início)")
    recuo = ""
    while len(rota) < n:
        atual = rota[-1]
        candidatas = [j for j in range(n) if not visitada[j]]
        candidatas.sort(key=lambda j: matriz[atual][j], reverse=True)   # da mais longe para a mais perto
        proxima = candidatas[-1]                                         # guloso: fica com a mais perto

        for j in candidatas:                                             # desenha as opções deste passo
            if j == proxima:
                print(f"{recuo}└── {j + 1} ({matriz[atual][j]})  ← escolhida")
            else:
                print(f"{recuo}├── {j + 1} ({matriz[atual][j]})")

        rota.append(proxima)
        visitada[proxima] = True
        recuo += "    "                                                  # o próximo passo fica embaixo da escolhida

    print(f"{recuo}└── volta para {inicio + 1} ({matriz[rota[-1]][inicio]})")
    return rota


def pedir_numero(mensagem, minimo, maximo):
    while True:
        texto = input(mensagem)
        if texto.isdigit() and minimo <= int(texto) <= maximo:
            return int(texto)
        print(f"Digite um número de {minimo} a {maximo}.")


if __name__ == "__main__":
    print()
    print("===== Guloso (vizinho mais próximo) em árvore =====")
    k = pedir_numero("Quantas cidades usar (2 a 12)? ", 2, 12)
    inicio = pedir_numero(f"Começar em qual cidade (1 a {k})? ", 1, k) - 1

    sub = [linha[:k] for linha in matriz[:k]]                            # só as k primeiras cidades
    print()
    rota = guloso_arvore(sub, inicio)
    print()
    print("Rota:", " → ".join(str(c + 1) for c in rota + [rota[0]]))
    print("Custo:", custo_rota(rota, sub))
