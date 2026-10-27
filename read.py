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