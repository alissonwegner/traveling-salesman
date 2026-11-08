from read import cidades, matriz      # reaproveita a leitura e a matriz do read.py
from custo import custo_rota
from mapa import desenhar


def guloso(matriz, inicio=0):
    n = len(matriz)
    rota = [inicio]                   # começa na cidade de início
    visitada = [False] * n
    visitada[inicio] = True

    while len(rota) < n:              # enquanto faltar cidade
        atual = rota[-1]
        proxima = None
        for j in range(n):            # procura a cidade não visitada mais perto da atual
            if not visitada[j] and (proxima is None or matriz[atual][j] < matriz[atual][proxima]):
                proxima = j
        rota.append(proxima)
        visitada[proxima] = True

    return rota                       # a volta para o início entra no custo_rota


if __name__ == "__main__":
    # contraexemplo: só as 4 primeiras cidades (a melhor rota custa 2315)
    m4 = [linha[:4] for linha in matriz[:4]]
    rota4 = guloso(m4)
    print("4 cidades:", [c + 1 for c in rota4], "custo", custo_rota(rota4, m4))

    # berlin52 inteiro (ótimo conhecido: 7542)
    rota = guloso(matriz)
    custo = custo_rota(rota, matriz)
    print("52 cidades:", [c + 1 for c in rota])
    print("Custo:", custo)
    print(f"Diferença do ótimo: {(custo - 7542) / 7542 * 100:.1f}%")
    desenhar(cidades, rota=rota, titulo=f"Guloso (vizinho mais próximo) - custo {custo}", arquivo="guloso.png")
