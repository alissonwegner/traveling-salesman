from read import cidades, matriz      # reaproveita a leitura e a matriz do read.py

n = len(cidades)


def escolher_cidade(mensagem):
    while True:
        texto = input(mensagem)
        if texto.isdigit() and 1 <= int(texto) <= n:
            return int(texto) - 1         # cidade 1 -> posição 0 da lista
        print(f"Digite um número de 1 a {n}.")


while True:
    print()
    print("===== Distância entre duas cidades =====")
    origem = escolher_cidade(f"Cidade de origem (1 a {n}): ")
    destino = escolher_cidade(f"Cidade de destino (1 a {n}): ")

    x1, y1 = cidades[origem]
    x2, y2 = cidades[destino]
    print(f"Cidade {origem + 1} ({x1:g}, {y1:g}) -> cidade {destino + 1} ({x2:g}, {y2:g})")
    print(f"Distância: {matriz[origem][destino]}")

    if input("Calcular outra? (s/n): ").strip().lower() != "s":
        break
