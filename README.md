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



## Algoritmos Implementados

### **Conceito: Dois vértices v_i e v_j têm uma aresta se:**
- e_ij ≠ ∅ ⟺ s·v_i + (1-s)·v_j ∈ cl(Q_free), ∀s ∈ [0,1]

### 1. Grafo de Visibilidade



### 2. Algoritmo de Kruskal/Prim



### 3. Busca em Largura (BFS)






