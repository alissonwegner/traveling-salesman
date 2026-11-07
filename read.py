import math

caminho = "berlin52.tsp.txt"
cidades = []                          # lista vazia: aqui vamos guardar as cidades

with open(caminho) as arquivo:        # 1. abre o arquivo (e fecha sozinho no final)
    for linha in arquivo:             # 2. pega uma linha por vez
        partes = linha.split()        # 3. quebra nos espaços: "1 565 575" -> ["1", "565", "575"]
        if len(partes) == 0:          #    linha vazia? pula para a próxima
            continue
        x = float(partes[1])          # 4. transforma o texto em número
        y = float(partes[2])
        cidades.append((x, y))        # 5. guarda a cidade no fim da lista

print("Total de cidades:", len(cidades))
print("Cidade 14 -> posicao 13 da lista:", cidades[13])





def distancia(a, b):
    dx = a[0] - b[0]                                  # diferença em x
    dy = a[1] - b[1]                                  # diferença em y
    return int(math.sqrt(dx ** 2 + dy ** 2) + 0.5)    # Pitágoras, arredondado

def matriz_distancias(cidades):
    n = len(cidades)
    matriz = [[0] * n for _ in range(n)]              # tabela n x n cheia de zeros
    for i in range(n):                                # cidade de onde sai (linha)
        for j in range(n):                            # cidade de destino (coluna)
            matriz[i][j] = distancia(cidades[i], cidades[j])
    return matriz


matriz = matriz_distancias(cidades)
print(matriz[0][1])   
print(matriz[3][4])