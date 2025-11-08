from collections import deque
from Modulos.models import Point


def close_vertex(ponto, mst_graph):
    """
    Encontra o vértice da arvore geradora mais próximo de um ponto dado.
    
    Args:
        ponto: Point - posicao do robo
        mst_graph: dicionario de adjacencias {vértice: {vizinho: peso}}
    
    Returns:
        vértice mais próximo (Point)
    """
    #se não tiver grafo, simplesmente não retorna nada (pode fazer um raise error na main se isso acontecer (ideia))
    if not mst_graph:
        return None
    
    vertices = list(mst_graph.keys())
    min_dist = float('inf')
    closest = None
    
    for v in vertices:
        dist = ponto.distance_to(v)
        if dist < min_dist:
            min_dist = dist
            closest = v
    
    return closest


def bfs_path(start, goal, mst_graph):
    """
    (BFS) para encontrar caminho entre dois vértices na arvore geradora minima.
    
    Args:
        start: vertice inicial (Point)
        goal: vertice final (Point)
        mst_graph: dicionario de adjacencias {vertice: {vizinho: peso}}
    
    Returns:
        path: lista de vértices do caminho, ou None se nao houver caminho
    """
    if start not in mst_graph or goal not in mst_graph: #mesma coisa lá de cima, se tiver algo errado com o grafo, inicio ou fim
        return None
    
    if start == goal:
        return [start]
    
    #bFS
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    
    while queue:
        current = queue.popleft()
        
        #se chegamos no objetivo
        if current == goal:
            #reconstruir caminho
            path = []
            node = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            return path
        
        #explorar vizinhos
        for neighbor in mst_graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    return None #não tem caminho