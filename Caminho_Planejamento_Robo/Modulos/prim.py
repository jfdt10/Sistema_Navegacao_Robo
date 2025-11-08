import heapq


def prim_mst(graph, start_vertex=None):
    """
    Em resumo: Cresce uma única árvore a partir de um vértice inicial,
    sempre adicionando a aresta de menor peso que conecta um vértice
    já incluído a um vértice ainda não incluído.
    
    Args:
        graph: VisibilityGraph com vértices e arestas
        start_vertex: vértice inicial (opcional, usa o primeiro se não especificado)
    
    Returns:
        mst_edges: lista de tuplas (v1, v2, peso) que formam a MST
    """
    vertices = graph.get_vertices()
    
    if not vertices:
        return []
    
    #escolher vertice inicial
    if start_vertex is None:
        start_vertex = vertices[0]
    
    #conjunto de vertices já incluídos na MST
    in_mst = set()
    in_mst.add(start_vertex)
    
    #heap de prioridade: (peso, vertice_origem, vertice_destino)
    pq = []
    
    #adicionar todas as arestas do vértice inicial ao heap
    for neighbor, weight in graph.adj[start_vertex].items():
        heapq.heappush(pq, (weight, start_vertex, neighbor))
    
    mst_edges = []
    total_weight = 0.0
    
    #enquanto não incluirmos todos os vértices
    while pq and len(in_mst) < len(vertices):
        # Extrair aresta de menor peso
        weight, v1, v2 = heapq.heappop(pq)
        
        #se v2 já está na MST, ignorar (evita ciclos)
        if v2 in in_mst:
            continue
        
        #adicionar aresta à MST
        mst_edges.append((v1, v2, weight))
        total_weight += weight
        in_mst.add(v2)
        
        #adicionar todas as novas arestas de v2 ao heap
        for neighbor, edge_weight in graph.adj[v2].items():
            if neighbor not in in_mst:
                heapq.heappush(pq, (edge_weight, v2, neighbor))
    
    print(f"Prim MST: {len(mst_edges)} arestas, peso total: {total_weight:.2f}")
    return mst_edges


def build_mst_graph(mst_edges):
    """
    Constroi um grafo a partir das arestas da MST.
    
    Args:
        mst_edges: lista de tuplas (v1, v2, peso)
    
    Returns:
        adj: dicionário {vértice: {vizinho: peso}}
    """
    adj = {}
    
    for v1, v2, weight in mst_edges:
        if v1 not in adj:
            adj[v1] = {}
        if v2 not in adj:
            adj[v2] = {}
        
        adj[v1][v2] = weight
        adj[v2][v1] = weight
    
    return adj