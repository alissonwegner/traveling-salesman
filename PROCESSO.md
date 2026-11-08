# Trabalho de AA: Caixeiro Viajante (TSP)

Roteiro do trabalho, seguindo as etapas do enunciado do professor.
O professor diz que as etapas não precisam ser feitas na ordem dele. Abaixo está a ordem sugerida, com o número da etapa original entre parênteses.

Marque `[x]` quando terminar um item.

**Próximo passo:** escrever o artigo (seção 7), começando pela modelagem (seção 3).

## Prazos

- **23/10/2026:** e-mail ao professor com o grupo, o problema e os algoritmos (conferir se foi enviado)
- **13/11/2026:** entrega do projeto (todo o código-fonte) e do artigo em PDF, pelo Moodle

O professor avisou que **não haverá apresentação**. O relatório deve ser entregue em **formato de artigo**.

## Plano até a entrega

| Dia | O que fazer |
|---|---|
| sáb 07/11 | Escolher os algoritmos · distância, matriz e custo de uma rota (seção 2) |
| dom 08/11 | Algoritmo heurístico: entender, pseudocódigo, programar e testar |
| seg 09/11 | Algoritmo exato: entender e escrever o pseudocódigo |
| ter 10/11 | Algoritmo exato: programar e testar com poucas cidades |
| qua 11/11 | Experimentos: medir tempos, custos e fazer os gráficos (seção 6) |
| qui 12/11 | Escrever o artigo (seção 7) |
| sex 13/11 | Revisar, gerar o PDF e entregar |

---

## 1. Definições iniciais (etapa 1)

- [x] Escolher o problema: caixeiro viajante (TSP)
- [ ] Definir o grupo (no máximo 4 pessoas)
- [x] Escolher o algoritmo **exato**: branch and bound (busca exaustiva com backtracking e poda)
- [x] Escolher o algoritmo **heurístico**: guloso (vizinho mais próximo)
- [ ] Confirmar que o e-mail foi enviado ao professor

## 2. Base que os dois algoritmos usam (início da etapa 4)

- [x] Ler o arquivo `berlin52.tsp.txt` e guardar as cidades numa lista (`read.py`)
- [x] Calcular a distância entre duas cidades (Pitágoras, arredondando para o inteiro mais próximo)
- [x] Montar a matriz de distâncias (todas as distâncias calculadas uma vez só)
- [x] Menu para consultar a distância entre duas cidades (`distancia.py`)
- [x] Calcular o custo de uma rota (somar as distâncias e voltar à cidade inicial) (`custo.py`)
- [x] Ler só as k primeiras cidades (sub-instâncias para o algoritmo exato)
- [ ] Copiar `st70.tsp.txt` e `pr76.tsp.txt` para esta pasta

## 3. Modelagem (etapa 2)

Escrever, para o relatório:

- [ ] **Entrada:** n cidades com suas posições (x, y)
- [ ] **Saída:** uma rota que passa por todas as cidades uma vez e volta ao início
- [ ] **Função objetivo:** minimizar o custo total da rota
- [ ] **Representação do grafo:** matriz de adjacência, com a justificativa da escolha
- [ ] **Tamanho do espaço de soluções:** (n − 1)!/2 rotas distintas
- [ ] **Classe de complexidade do problema:** NP-difícil

## 4. Projeto e análise teórica (etapa 3)

Para **cada** um dos dois algoritmos:

- [ ] Entender a ideia do algoritmo
- [ ] Escrever o pseudocódigo
- [ ] Dizer qual é o paradigma de projeto (guloso; busca exaustiva com backtracking e poda)
- [ ] Calcular a complexidade de **tempo** e de **espaço** no pior caso

Além disso:

- [ ] **Exato:** explicar por que ele sempre acha a melhor rota (corretude)
- [ ] **Heurístico:** mostrar um exemplo em que ele **não** acha a melhor rota (contraexemplo)

## 5. Implementação (etapa 4)

- [x] Programar o algoritmo exato, seguindo o pseudocódigo (`bnb.py`, e `bnb_arvore.py` para ver a árvore)
- [x] Programar o algoritmo heurístico, seguindo o pseudocódigo (`guloso.py`)
- [x] Usar o custo da rota do guloso como "melhor até agora" inicial do branch and bound, para ele podar mais desde o começo
- [ ] Testar em instâncias pequenas e conferir com a resposta feita à mão
- [ ] Anotar as decisões que mudam o custo (ex.: como escolher a próxima cidade, critério de poda)

## 6. Experimentos (etapa 5)

- [x] Comparar guloso e B&B nas mesmas cidades: rota, custo (ida e volta), tempo, diferença % e mapa lado a lado (`comparar.py`)
Tudo abaixo roda com `python experimentos.py` (~1 min), que gera `resultados.csv` e os gráficos.

- [x] Rodar o exato em sub-instâncias de tamanho crescente: 4 a 13 cidades
- [x] Rodar o heurístico nas sub-instâncias e no berlin52 inteiro: 4 a 52 cidades
- [ ] (Opcional) Rodar o heurístico no st70 e no pr76
- [x] Medir o tempo com média e desvio padrão: 5 repetições no B&B, 30 no guloso
- [x] Medir a qualidade: custo da rota e diferença % em relação ao ótimo
- [x] Fazer os gráficos: `tempo_bnb.png`, `tempo_guloso.png`, `qualidade_guloso.png`
- [ ] Comparar as curvas com a complexidade prevista na etapa 3 (texto do artigo)
- [x] Maior tamanho em tempo razoável: B&B até 13 cidades (~10 s); guloso resolve as 52 em ~0,15 ms

Diferença % = (custo encontrado − ótimo) / ótimo × 100

Ótimos conhecidos (TSPLIB, distância arredondada):

| Instância | Cidades | Ótimo |
|---|---|---|
| berlin52 | 52 | 7542 |
| st70 | 70 | 675 |
| pr76 | 76 | 108159 |

## 7. Artigo em PDF (etapa 6)

- [ ] Confirmar com o professor qual modelo de artigo usar (ex.: SBC ou IEEE) e se há limite de páginas

Seções do artigo, e de onde vem o conteúdo de cada uma:

- [ ] **Título e resumo:** o problema, os dois algoritmos e o principal resultado, em um parágrafo
- [ ] **1. Introdução:** o que é o TSP, por que ele é difícil e o que o artigo faz
- [ ] **2. Modelagem do problema:** entrada, saída, função objetivo, matriz de adjacência, espaço de soluções e classe de complexidade (seção 3 deste roteiro)
- [ ] **3. Algoritmos:** para cada um, a ideia, o pseudocódigo, o paradigma, a corretude ou o contraexemplo, e a complexidade de tempo e de espaço (seção 4)
- [ ] **4. Implementação:** a linguagem e as decisões que mudam o custo (seção 5)
- [ ] **5. Experimentos:** as instâncias usadas, como foi medido (repetições, média e desvio padrão, computador usado) e os resultados em tabelas e gráficos (seção 6)
- [ ] **6. Discussão:** a teoria bateu com a prática? Qual o maior tamanho que cada algoritmo resolve?
- [ ] **7. Conclusão:** o que foi aprendido e o que poderia melhorar
- [ ] **Referências:** enunciado, TSPLIB e os livros ou artigos consultados

## 8. Entrega

- [ ] Gerar o PDF do artigo
- [ ] Juntar todo o código-fonte
- [ ] Enviar pelo Moodle até 13/11/2026
