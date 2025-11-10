# Planejamento de Caminho para Robôs Autônomos
Sistema de navegação baseado em Grafos de Visibilidade e Árvores Geradoras Mínimas para planejamento de trajetórias em ambientes com obstáculos poligonais.

## 👥 Autores:

- Jean Felipe Duarte Tenório 
- Alison Bruno Martires Soares


 Instituição: UFAL
 
 Disciplina: Teoria dos Grafos
 
 Professor: Glauber Rodrigues Leite
 
 Data: Novembro/2025


## 📋 Descrição do Projeto:
Este projeto implementa um sistema completo de planejamento de caminho para veículos autônomos navegando em ambientes 2D com obstáculos. O sistema utiliza conceitos de teoria dos grafos para criar um roadmap que permite ao robô navegar de qualquer ponto a outro, evitando colisões.



## 🚀 Como Executar:

### Pré-requisitos

### Python 3.8 ou superior:
```
python --version
```
### Instalar dependências:

```
pip install -r requirements.txt

```

### Navegar para Pasta e Executar a Main:

```
cd Caminho_Planejamento_Robo

python robot_navegation.py

```
## 📁 Estrutura do Projeto:

```
Caminho_Planejamento_Robo/
├── robot_navegation.py           ← Main(Arquivo Principal)
├── Mapa/
|   ├── bitmap.pdf
|   ├── bitmap.png
|   ├── bitmap.svg
|   ├── map1.txt
├── Modulos/
│   ├── __init__.py
│   ├── models.py                 ← Classes Point e Obstacles
│   ├── visibility_graph.py       ← VisibilityGraph
│   ├── kruskal.py                ← kruskal
|   ├── prim.py                   ← prim               
│   ├── pathfinding.py            ← BFS, vertice_mais_proximo
├── Resultados/                   
|   ├── 01_visibilidade.png
|   ├── 02_mst_kruskal.png
|   ├── 02_mst_prim.png
|   ├── 03_caminho_kruskal.png
|   ├── 03_caminho_prim.png
|   ├── 04_resultado_unificado_kruskal.png
|   ├── 04_resultado_unificado_prim.png
|   ├── mapa_plotado.png
├── Testes/                       
|   ├── test.py ← Testes de Funcionalidades
|
├── Utils/                       
│   ├── __init__.py
│   └── file_reader.py    ← Leitura do arquivo map1.txt
│   └── plotar_caminho.py ← Plotagem caminho(Arquvo Excecução(Testes))
│   └── plotar_mapa.py  ← Lógica Principal integra plotagem de mapa,grafos visibilidade,MST,caminho c
│   └── plotar_mst.py   ← Plotagem Árvore Geradora Mínima(Arquivo Execução(Testes))
│   └── plotar_visibilidade.py ← plotagem Grafo de Visibilidade(Arquivo Execução(Testes))
├── README.md
|── LICENSE
└── requirements.txt
```

📄 Formato do Arquivo de Mapa:
```
q_start_x, q_start_y          # Posição inicial
q_goal_x, q_goal_y            # Posição final
<numero_de_obstaculos>        # Quantidade de obstáculos
<numero_de_vertices_obs_1>    # Vértices do obstáculo 1
x1, y1
x2, y2
...
<numero_de_vertices_obs_2>    # Vértices do obstáculo 2
x1, y1
...
```
## 🔍 Resultados Visuais:


### 1. Mapa com Obstáculos:

<p align="center">
  <img src="Caminho_Planejamento_Robo/Resultados/mapa_plotado.png" alt="Mapa com Obstáculos:" width="600"/>
</p>


### 2. Grafo de Visibilidade:

<p align="center">
  <img src="Caminho_Planejamento_Robo/Resultados/01_visibilidade.png" alt="Mapa Grafo de Visibilidade:" width="600"/>
</p>


### 3. Árvore Geradora Mínima (Kruskal / Prim):

#### 3.1 Kruskal:

<p align="center">
  <img src="Caminho_Planejamento_Robo/Resultados/02_mst_kruskal.png" alt="Mapa Árvore Geradora Mínima:" width="600"/>
</p>

#### 3.2 Prim:

<p align="center">
  <img src="Caminho_Planejamento_Robo/Resultados/02_mst_prim.png" alt="Mapa Árvore Geradora Mínima:" width="600"/>
</p>


### 4. Caminho Encontrado:

#### 4.1 Caminho Encontrado Resultado Kruskal:

<p align="center">
  <img src="Caminho_Planejamento_Robo/Resultados/04_resultado_unificado_kruskal.png" alt="Mapa Caminho Encontrada na Árvore Geradora Mínima :" width="600"/>
</p>

#### 4.1 Caminho Encontrado Resultado Prim:

<p align="center">
  <img src="Caminho_Planejamento_Robo/Resultados/04_resultado_unificado_prim.png" alt="Mapa Caminho Encontrada na Árvore Geradora Mínima :" width="600"/>
</p>

## Implementação dos Algoritmos

### **Conceito Base: Visibilidade entre Vértices**
Dois vértices v_i e v_j têm uma aresta se: **e_ij ≠ ∅ ⟺ s·v_i + (1-s)·v_j ∈ cl(Q_free), ∀s ∈ [0,1]**

---

### Algoritmo de Grafo de Visibilidade:

### Pseudocódigo Teórico:

```
início [ dados: V (conjunto de vértices), O (conjunto de obstáculos) ]

  E ← ∅; 

  para todo v_i ∈ V fazer
  início
    para todo v_j ∈ V tal que i < j fazer
    início
      
      se TemVisibilidade(v_i, v_j, O) então
      início
        peso ← DistanciaEuclidiana(v_i, v_j);
        E ← E ∪ (v_i, v_j, peso);
      fim;
      
    fim;
  fim;

  retornar G = (V, E);
fim.
```

### O que foi implementado (visibility_graph.py):

###  Estruturas de Dados Utilizadas

- `VisibilityGraph`Classe principal que armazena o grafo de visibilidade.

- Representação: dicionário de adjacências `self.adj`
- Cada chave: um vértice (`Point`)
- Cada valor: outro dicionário mapeando vértices vizinhos e pesos (distâncias)

- `Point` Classe (importada de `Modulos.models`) que representa um ponto 2D:
- Atributos: `x`, `y`
- Método: `distance_to()` — calcula a distância euclidiana entre dois pontos

- `LineString` Objeto da biblioteca **Shapely** usado para representar o **segmento de reta** entre dois pontos e detectar interseções com obstáculos.

- `list` Usada para agregar todos os vértices (`all_vertices`) antes de verificar a visibilidade entre pares.

**Fluxo do Algoritmo:**

1. Inicializa um grafo vazio.
2. Adiciona os vértices iniciais e finais (`q_start` e `q_goal`).
3. Para cada obstáculo:
   - Adiciona seus vértices ao grafo.
   - Conecta vértices consecutivos (arestas que formam as bordas do obstáculo).
4. Gera uma lista de **vértices únicos** (sem repetição).
5. Para cada par de vértices distintos:
   - Verifica se já existe uma aresta entre eles.
   - Se não existir, chama `is_visible(v1, v2, obstacles)`.
   - Caso haja visibilidade, adiciona a aresta com peso igual à distância euclidiana.
6. Retorna o grafo completo.


**Diferenças chave em relação ao pseudocódigo:**

- Uso de **classes e estruturas de dados modernas** (`VisibilityGraph`, `Point`) em vez de conjuntos abstratos.  
- Implementação da **verificação de visibilidade** com a biblioteca **Shapely**, garantindo interseção geométrica precisa.  
- **Arestas dos obstáculos** são adicionadas explicitamente ao grafo, preservando sua geometria.  
- Controle de **duplicatas de vértices e arestas** para evitar redundâncias.  
- Inclusão de **tolerância numérica (1e-9)** para lidar com erros de ponto flutuante.  
- Estrutura **modular** com funções independentes (`is_visible`, `build_visibility_graph`).  
- Adição de **mensagens de log** para acompanhamento da execução.  
- Retorno do grafo como **objeto estruturado (`VisibilityGraph`)**, e não apenas como um par `(V, E)`.  

## Função Auxiliar: `is_visible`
```
procedimento TemVisibilidade(p1, p2, Obstaculos)
  início
    Segmento ← (p1, p2); 
    para todo Obj ∈ Obstaculos fazer
    início
      se Segmento intercepta interior(Obj) então
      início
        retornar falso;
      fim;
    fim;
    
    retornar verdadeiro;
  fim.
```
### O que foi implementado (em visibility_graph.py):

**Funcionalidade `is_visible(p1,p2,obstacles)`:**

- A função `is_visible` verifica se **dois pontos possuem linha de visada livre** entre si — ou seja, se o segmento de reta que conecta `p1` e `p2` não atravessa o interior de nenhum obstáculo.

- Ela é essencial na construção do **grafo de visibilidade**, pois determina quais vértices podem ser conectados por arestas válidas no espaço livre \(Q_{free}\).

**Implementação:**

1. **Criação do Segmento:**  
   Um segmento é criado entre os pontos `p1` e `p2` usando `LineString` (da biblioteca *Shapely*).

2. **Verificação de Interseção:**  
   Para cada obstáculo do ambiente:
   - Calcula-se a interseção entre o segmento e o polígono do obstáculo.
   - Se a interseção for **vazia**, o segmento não cruza o obstáculo.
   - Se houver interseção, o tipo geométrico é analisado:
     - **Ponto único:** é permitido se o ponto de interseção for exatamente um dos extremos (`p1` ou `p2`).
     - **Múltiplos pontos ou segmentos:** indica cruzamento com o interior do obstáculo → **visibilidade bloqueada**.

3. **Tolerância Numérica:**  
   Pequenas diferenças numéricas são tratadas com uma margem de erro de `1e-9` para evitar falsos bloqueios em vértices coincidentes.

4. **Resultado:**  
   - Retorna `True` se o segmento estiver totalmente em região livre.  
   - Retorna `False` se houver qualquer interseção indevida com os obstáculos.

**Utilidade para o Grafo de Visibilidade:**
- A função `is_visible` é extremamente importante e garante que apenas **arestas totalmente livres de colisões** sejam adicionadas ao grafo de visibilidade, assegurando que o caminho planejado permaneça dentro da área navegável.

## Algoritmo de Kruskal(MST)

### Pseudocódigo Teórico:

```
Início [ dados: grafo G = (V,E) valorado nas arestas ]
para todo i de 1 a n fazer v(i) ← i; t ← 0; k ← 0; T ← ∅; [ T: arestas da árvore ]
ordenar o conjunto de arestas em ordem não-decrescente;
enquanto t < n - 1 fazer [ t: contador de arestas da árvore ]
  início
    k ← k + 1; [ k: contador de iterações ; u(k) = (i,j) aresta da vez ]
    se v(i) ≠ v(j) então
    início
      para todo v(q) | v(q) = max [ v(i), v(j) ] fazer v(q) = min [ v(i), v(j) ]
        T ← T ∪ (i,j); [ adiciona a aresta à árvore ]
        t ← t + 1;
    fim;
   fim;
fim.
```

### O que foi implementado (kruskal.py):

###  Estruturas de Dados Utilizadas:

- Lista de arestas como tuplas (u, v, peso).
- Estrutura Union‑Find (Disjoint Set) com compressão de caminho e `rank` para união eficiente.
- Resultado: lista de arestas da MST e custo total.

**Fluxo do algoritmo na implementação:**
1. Converter o grafo (vertices/arestas) em uma lista de arestas indexadas por inteiros.
2. Ordenar a lista de arestas por peso (ordem não‑decrescente).
3. Inicializar Union‑Find com n componentes.
4. Iterar sobre as arestas ordenadas:
   - Se find(u) != find(v): executar union(u, v) e adicionar a aresta à MST.
   - Parar quando MST tiver n-1 arestas ou terminar a lista.
5. Converter a lista de arestas da MST de índices de volta para os objetos Point e montar o dicionário de adjacência usado pelo restante do sistema.

**Otimização Implementada:**
- Ordenação: O(E log E)
- Unions/Finds durante a varredura: O(E · alpha(V)) ≈ O(E)
- Portanto: O(E log E) no geral.
- O pseudocódigo que atualiza rótulos de componentes por varredura pode requerer atualizações em O(V) para cada aresta aceita → pior caso O(E·V).
- Union‑Find elimina essas atualizações custosas, tornando o algoritmo escalável para grafos grandes.


**Diferenças chave em relação ao pseudocódigo:**
- O pseudocódigo usa um vetor de rótulos v(i) e faz atualizações em massa — abordagem correta, porém ineficiente para grafos grandes.
- A implementação substitui os rótulos por Union‑Find, garantindo operações amortizadas quase constantes (find/union), reduzindo complexidade prática.
- Complexidade prática:
  - Pseudocódigo abordagem menos otimizada: até O(E·V) em pior caso ao atualizar rótulos.
  - Implementação: O(E log E) para ordenar + quase O(1) amortizado por operação Union‑Find.
- A conversão entre representação (Point -> índice) é feita antes da execução do Kruskal; após obter a MST por índices, o código reconstrói a estrutura de adjacência com objetos Point para integração com BFS e plotagem.



## Algoritmo de Prim (MST)

### Pseudocódigo Teórico:
```
início [ dados: grafo G = (V,E) valorado nas arestas ] ; valor ← ∞; custo ← 0;
T ← {1}; E(T) ← ∅; T e E(T): vértices e arestas da árvore ]
enquanto | T | < n – 1 fazer
  início
  para todo k ∈ T fazer [ examinar vértices já escolhidos ]
  início
    para todo i ∈ V – T fazer [ examinar vértices ainda não escolhidos ]
    se v_ki < valor então
    início
      valor ← v_ki; vesc ← k; vnovo ← i;
    fim;
  fim;
  custo ← custo + valor; T ← T ∪ {vnovo}; E(T) ← E(T) ∪ (vesc, vnovo); valor ← ∞;
  fim;
fim.
```

### O que foi implementado (prim.py):

**Estruturas de Dados Utilizadas:**
- `in_mst`: conjunto (set) para armazenar vértices já incluídos na árvore (equivalente ao T do pseudocódigo)
- `pq`: heap de prioridade (heapq) para armazenar arestas candidatas com seus pesos (tuplas: `(peso, origem, destino)`)
- `mst_edges`: lista para armazenar as arestas que formam a MST final

**Otimização Implementada:**

Em vez de varrer todos os vértices a cada iteração (como no pseudocódigo original O(n²)), utilizamos um **heap de prioridade** que automaticamente mantém as arestas ordenadas por peso. Isso melhora a complexidade para **O(E log V)**.

**Fluxo do Algoritmo:**

1. **Inicialização:**
   - Seleciona o primeiro vértice do grafo como ponto de partida (ou um vértice específico, se fornecido)
   - Adiciona esse vértice ao conjunto `in_mst`
   - Insere todas as arestas conectadas a esse vértice no heap

2. **Loop Principal:**
   - Enquanto houver arestas no heap e ainda existirem vértices não incluídos:
     - Remove a aresta de **menor peso** do heap (`heapq.heappop`)
     - Verifica se o vértice destino já está na MST (evita ciclos)
     - Se não estiver, adiciona a aresta à MST e o vértice ao conjunto `in_mst`
     - Insere todas as novas arestas do vértice recém-adicionado no heap

3. **Construção do Grafo MST:**
   - A função `build_mst_graph()` converte a lista de arestas em um dicionário de adjacências bidirecional
   - Cada aresta (v1, v2, peso) gera duas entradas: `adj[v1][v2]` e `adj[v2][v1]`

**Diferenças chave em relação ao pseudocódigo:**
- Uso de heap ao invés de busca linear para encontrar a aresta de menor peso
- Verificação explícita de ciclos com `if v2 in in_mst`
- Acumulação do peso total da MST para estatísticas

---

## Busca em Largura - BFS (Pathfinding)

### Pseudocódigo Teórico:
```
início [ dados: grafo G = (V,E) e um vértice fonte s ∈ V ]

  para todo v ∈ V faça
    explorado[v] ← falso; d[v] ← ∞;
  fim;
  
  explorado[s] ← verdadeiro;
  d[s] ← 0;
  
  Q ← ∅; [ Q: uma fila ]
  ENFILEIRAR(Q, s);
  
  enquanto Q ≠ ∅ fazer
  início
    u ← DESENFILEIRAR(Q); [ u: vértice sendo processado ]
    
    para todo v adjacente a u fazer
    início
      se não explorado[v] então
      início
        explorado[v] ← verdadeiro;
        d[v] ← d[u] + 1;
        ENFILEIRAR(Q, v); [ insere v no fim da fila ]
      fim;
    fim;
  fim;
  
fim.
```

### O que foi implementado (pathfinding.py):

**Estruturas de Dados Utilizadas:**
- `queue`: fila implementada com `deque` (double-ended queue) do módulo collections
- `visited`: conjunto (set) para armazenar vértices já explorados (equivalente ao `explorado[]` do pseudocódigo)
- `parent`: dicionário que mapeia cada vértice ao seu predecessor no caminho (usado para reconstruir o caminho final)

**Funcionalidade `bfs_path(start, goal, mst_graph)`:**

1. **Validações Iniciais:**
   - Verifica se os vértices inicial e final existem no grafo
   - Trata o caso especial onde início e fim são o mesmo vértice
   - Retorna `None` se não houver caminho válido

2. **Inicialização do BFS:**
   - Adiciona o vértice inicial (`start`) à fila
   - Marca o vértice inicial como visitado
   - Define o pai do vértice inicial como `None` (não tem predecessor)

3. **Exploração em Largura:**
   - Remove o primeiro vértice da fila (`queue.popleft()`)
   - Se for o vértice objetivo, reconstrói o caminho usando o dicionário `parent`
   - Caso contrário, explora todos os vizinhos não visitados:
     - Marca cada vizinho como visitado
     - Registra o vértice atual como pai do vizinho
     - Adiciona o vizinho à fila para exploração futura

4. **Reconstrução do Caminho:**
   - Ao encontrar o objetivo, percorre o dicionário `parent` de trás para frente
   - Começa no `goal` e vai até o `start` (onde `parent[start] = None`)
   - Inverte a lista para obter o caminho na ordem correta

---

## Função Auxiliar: `close_vertex`

### O que foi implementado (pathfinding.py):

**Funcionalidade `close_vertex(ponto, mst_graph)`:**

Esta função não está presente no pseudocódigo teórico, mas é essencial para conectar a posição do robô (que pode estar em qualquer ponto do espaço livre) à MST construída.

**Implementação:**
- Recebe a posição atual do robô (um `Point`) e o grafo MST
- Itera sobre todos os vértices do grafo
- Calcula a distância euclidiana entre o ponto do robô e cada vértice
- Retorna o vértice mais próximo (menor distância)

**Utilidade no Sistema:**
- Permite que o robô "se conecte" à MST a partir de qualquer posição
- É chamada tanto para a posição inicial quanto para a posição final
- Garante que sempre haja um ponto de entrada/saída válido na árvore geradora
