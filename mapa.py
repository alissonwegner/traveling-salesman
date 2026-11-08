import matplotlib.pyplot as plt

from read import cidades              # reaproveita a leitura do read.py


def desenhar(cidades, rota=None, titulo="berlin52", arquivo="mapa.png"):
    xs = [c[0] for c in cidades]      # todos os x
    ys = [c[1] for c in cidades]      # todos os y

    plt.figure(figsize=(10, 7))

    # se recebeu uma rota, liga as cidades nessa ordem e volta para a primeira
    if rota is not None:
        caminho = rota + [rota[0]]
        plt.plot([xs[i] for i in caminho], [ys[i] for i in caminho], color="tab:green", linewidth=1.5, zorder=1)

    plt.scatter(xs, ys, color="tab:blue", s=30, zorder=2)                 # as cidades
    for i, (x, y) in enumerate(cidades):
        plt.text(x + 12, y + 12, str(i + 1), fontsize=8)                  # número da cidade (posição 0 = cidade 1)

    plt.title(titulo)
    plt.gca().set_aspect("equal")     # mesma escala em x e y, para o mapa não ficar esticado
    plt.savefig(arquivo, dpi=150, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    desenhar(cidades)
