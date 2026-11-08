# Caixeiro Viajante (TSP) com berlin52

Trabalho de Projeto e Análise de Algoritmos.

## O problema em uma frase

Temos 52 pontos de Berlim. Queremos a **rota mais curta** que passa por **todos** eles **uma vez** e **volta ao início**.

Para quem vem de infraestrutura, pense assim:

| No código | Analogia de infra |
|---|---|
| Cidade | Um servidor (nó da rede) |
| Distância entre duas cidades | A latência entre dois servidores |
| Matriz de distâncias | Uma tabela de latência full-mesh: todos contra todos, medida uma vez só |
| Rota | Um **anel** que passa por todos os servidores e fecha no primeiro |
| Custo da rota | A soma das latências de todos os links do anel, incluindo o link de volta |

O difícil é que o número de anéis possíveis explode. Com 10 cidades são 362 mil. Com 13 são 479 milhões. Com 52 são cerca de 10⁶⁶. Não existe máquina que teste tudo isso.

## Os dois algoritmos

### Guloso (vizinho mais próximo): rápido, mas não garante a melhor rota

Sai da cidade 1 e **sempre vai para a cidade mais perto que ainda não visitou**. É como escolher sempre o próximo hop de menor latência.

- **Vantagem:** resolve as 52 cidades na hora.
- **Problema:** ele escolhe sem olhar para frente. No fim, sobram cidades longe e o link de volta fica caro.
- **Resultado no berlin52:** 8980, contra o melhor possível, 7542. Ficou **19,1% pior**.

### Branch and bound (B&B): sempre acha a melhor rota, mas é lento

Testa as rotas possíveis, uma cidade por vez, mas **aborta um caminho assim que ele fica mais caro que a melhor rota já encontrada**. Funciona como um timeout: não adianta continuar um caminho que já perdeu.

- **Ponto de partida:** ele usa a rota do guloso como "melhor até agora". Assim, já começa abortando caminhos ruins.
- **Primeira cidade fixa:** a cidade 1 é sempre o começo. Como a rota é um anel, começar em outra cidade dá o mesmo anel.
- **Vantagem:** a resposta é **sempre a melhor possível**.
- **Problema:** o tempo cresce de forma explosiva. Até umas 13 cidades é viável. Com 52 cidades, não termina.

## Como rodar

**Requisitos:** Python 3 (testado no 3.13) e a biblioteca de gráficos matplotlib.

```bash
pip install matplotlib
```

Rode sempre **de dentro da pasta do projeto**, porque o código procura o arquivo `berlin52.tsp.txt` nela.

```bash
cd traveling-salesman
```

```bash
python comparar.py
```

## O que cada arquivo faz

| Arquivo | O que faz | O que pergunta | O que gera |
|---|---|---|---|
| `berlin52.tsp.txt` | Os dados: uma cidade por linha, no formato `número x y` | — | — |
| `read.py` | Lê o arquivo e monta a matriz de distâncias. **Todos os outros dependem dele** | — | — |
| `custo.py` | Soma o custo de uma rota, com a volta | — | — |
| `distancia.py` | Consulta a distância entre duas cidades | Origem e destino | Texto |
| `mapa.py` | Desenha as 52 cidades | — | `mapa.png` |
| `guloso.py` | Roda o guloso nas 52 cidades | — | `guloso.png` |
| `guloso_arvore.py` | Mostra o guloso passo a passo no terminal | Quantas cidades (até 12) e por qual começar | Texto |
| `bnb.py` | Roda o B&B | Quantas cidades (use até 13) | `bnb.png` |
| `bnb_arvore.py` | Mostra cada caminho que o B&B testa ou aborta | Quantas cidades (até 7) e se usa o guloso como ponto de partida | Texto |
| `comparar.py` | Roda os dois nas mesmas cidades e compara | Quantas cidades (até 13) e por qual começar | Tabela e `comparar.png` |
| `experimentos.py` | Mede os dois algoritmos em vários tamanhos, repetindo cada medição (média e desvio padrão). Leva ~1 min | — | `resultados.csv`, `tempo_bnb.png`, `tempo_guloso.png`, `qualidade_guloso.png` |
| `PROCESSO.md` | O roteiro e o checklist do trabalho | — | — |

O "quantas cidades" sempre usa **as primeiras** do arquivo. Por exemplo, 10 significa as cidades de 1 a 10.

### Quem usa quem

```
berlin52.tsp.txt
   └── read.py .......................... lê as cidades e monta a matriz (todos usam)
         ├── custo.py, mapa.py .......... peças reaproveitadas pelos outros
         ├── distancia.py
         ├── guloso.py, guloso_arvore.py
         └── bnb.py, bnb_arvore.py ...... usam o guloso como ponto de partida
               └── comparar.py, experimentos.py ... usam o guloso e o B&B
```

## Detalhes que mudam o resultado

- **Distância:** é a linha reta entre os dois pontos (Pitágoras), arredondada para o inteiro mais próximo. É o padrão da biblioteca de onde vem o berlin52 (TSPLIB). Sem esse arredondamento, os números não batem com o ótimo oficial de 7542.
- **As coordenadas não são GPS.** São posições num plano, em uma unidade qualquer.
- **Matriz em vez de lista:** todas as distâncias são calculadas uma vez só, no início. Depois, cada consulta é imediata, como ler uma célula de planilha.

## Resultados de referência

Medido neste computador. Os tempos variam de máquina para máquina. Para refazer todas as medições, rode `python experimentos.py`.

| Cidades | Guloso | B&B (melhor rota) | Guloso pior em | Tempo do B&B | Caminhos que o B&B testou | Rotas possíveis |
|---|---|---|---|---|---|---|
| 4 | 2598 | 2315 | 12,2% | < 0,001 s | 16 | 6 |
| 7 | 2632 | 2322 | 13,4% | 0,001 s | 1.040 | 720 |
| 10 | 3278 | 2826 | 16,0% | 0,05 s | 95.940 | 362.880 |
| 13 | 4791 | 4564 | 5,0% | ~9,4 s | 21.982.527 | 479.001.600 |
| 52 | 8980 | 7542 (ótimo oficial) | 19,1% | não termina | — | ~10⁶⁶ |

Com poucas cidades, o B&B testa **mais** caminhos do que existem rotas. Isso acontece porque ele também conta os caminhos parciais, inclusive os que abortou no meio. A economia aparece quando cresce: com 13 cidades, testou 22 milhões de caminhos em vez de passar pelas 479 milhões de rotas.

## Problemas comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `No module named 'matplotlib'` | Falta a biblioteca de gráficos | `pip install matplotlib` |
| `FileNotFoundError: berlin52.tsp.txt` | Rodou de fora da pasta do projeto | Entre na pasta com `cd` e rode de novo |
| Toda execução começa com "Total de cidades: 52" e dois números | É o `read.py` conferindo a leitura | Normal, pode ignorar |
| O terminal parece travado depois do resultado | A janela do gráfico está aberta | Feche a janela do gráfico |
| O B&B não termina | Cidades demais | `Ctrl+C` para parar, e use até 13 cidades |
| Pasta `__pycache__` | Cache que o Python cria sozinho | Pode ignorar ou apagar |
