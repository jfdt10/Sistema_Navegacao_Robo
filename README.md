# Planejamento de Caminho para Robôs Autônomos
Sistema de navegação baseado em Grafos de Visibilidade e Árvores Geradoras Mínimas para planejamento de trajetórias em ambientes com obstáculos poligonais.

## 👥 Autores

- Jean Felipe Duarte Tenório 
- Alison Bruno Martires Soares


 Instituição: UFAL
 
 Disciplina: Teoria dos Grafos
 
 Professor: Glauber Rodrigues Leite
 
 Data: Novembro/2025


## 📋 Descrição do Projeto
Este projeto implementa um sistema completo de planejamento de caminho para veículos autônomos navegando em ambientes 2D com obstáculos. O sistema utiliza conceitos de teoria dos grafos para criar um roadmap que permite ao robô navegar de qualquer ponto a outro, evitando colisões



## 🚀 Como Executar

### Pré-requisitos

### Python 3.8 ou superior
```
python --version
```
### Instalar dependências

```
pip install -r requirements.txt
```

## 📁 Estrutura do Projeto
Caminho_Planejamento_Robo/
├── robot_navegation.py           ← Main(Arquivo Principal)
├── Docs/
|   ├──Explicacao_Algoritmos.md   ← Arquivo que Explica e Compara Algoritmos com Pseudocódigo
├── Mapa/
|   ├── map1.png
|   ├── map1.txt
├── Modulos/
│   ├── __init__.py
│   ├── models.py                 ← Classes Point e Obstacles
│   ├── visibility_graph.py       ← VisibilityGraph
│   ├── kruskal.py                ← kruskal
|   ├── prim.py                   ← prim               
│   ├── pathfinding.py            ← BFS, vertice_mais_proximo
│   └── visualization_map.py      ← Visualização do Mapa
├── Resultados/                   
|   ├── result1.png
├── Testes/                       ← Testes de Funcionalidades
|   ├── test.py
|
├── Utils/                        ← Leitura do arquivo map1.txt
│   ├── __init__.py
│   └── file_reader.py   
├── README.md
|── LICENSE
└── requirements.txt


📄 Formato do Arquivo de Mapa
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
## 🔍 Resultados Visuais


### 1. Mapa com Obstáculos




### 2. Grafo de Visibilidade




### 3. Árvore Geradora Mínima (Kruskal / Prim)



### 4. Caminho Encontrado



## Algoritmos Implementados(Pseudocódigos)

### **Conceito: Dois vértices v_i e v_j têm uma aresta se:**
- e_ij ≠ ∅ ⟺ s·v_i + (1-s)·v_j ∈ cl(Q_free), ∀s ∈ [0,1]

### 1. Grafo de Visibilidade  

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

### 2. Algoritmo de Kruskal/Prim

#### 2.1 Kruskal

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
#### 2.2 Prim

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


### 3. Busca em Largura (BFS)

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



