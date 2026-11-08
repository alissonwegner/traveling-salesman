from read import matriz               # reaproveita a matriz do read.py


def custo_rota(rota, matriz):
    total = 0
    for k in range(len(rota) - 1):
        total += matriz[rota[k]][rota[k + 1]]     # trecho da cidade atual até a próxima
    total += matriz[rota[-1]][rota[0]]            # volta da última para a primeira
    return total


if __name__ == "__main__":
    rota = [0, 1, 2, 3]                           # 1 -> 2 -> 3 -> 4 -> 1
    print("Rota 1-2-3-4:", custo_rota(rota, matriz))      # deve dar 2315

    rota = list(range(len(matriz)))               # 1 -> 2 -> ... -> 52 -> 1
    print("Rota 1..52:", custo_rota(rota, matriz))        # deve dar 22205
