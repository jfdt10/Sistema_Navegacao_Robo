from shapely.geometry import LineString
from Modulos.models import Point

class VisibilityGraph:
    def __init__(self):
        self.adj = {}
    
    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = {}
    
    def add_edge(self, v1, v2, weight):
        self.add_vertex(v1)
        self.add_vertex(v2)
        self.adj[v1][v2] = weight
        self.adj[v2][v1] = weight
    
    def get_edges(self):
        edges = []
        seen = set()
        for v1, neighbors in self.adj.items():
            for v2, weight in neighbors.items():
                edge_key = tuple(sorted([id(v1), id(v2)]))
                if edge_key not in seen:
                    edges.append((v1, v2, weight))
                    seen.add(edge_key)
        return edges
    
    def get_vertices(self):
        return list(self.adj.keys())

def is_visible(p1, p2, obstacles):
    if p1 == p2:
        return False
    
    line = LineString([(p1.x, p1.y), (p2.x, p2.y)])
    
    for obstacle in obstacles:
        inter = obstacle.shapely_polygon.intersection(line)
        if inter.is_empty:
            continue
        if inter.geom_type == 'Point':
            pt_x, pt_y = inter.x, inter.y
            if (abs(pt_x - p1.x) < 1e-9 and abs(pt_y - p1.y) < 1e-9) or \
               (abs(pt_x - p2.x) < 1e-9 and abs(pt_y - p2.y) < 1e-9):
                continue
            return False
        if inter.geom_type == 'MultiPoint':
            ok = True
            for pt in inter.geoms:
                if not ((abs(pt.x - p1.x) < 1e-9 and abs(pt.y - p1.y) < 1e-9) or \
                        (abs(pt.x - p2.x) < 1e-9 and abs(pt.y - p2.y) < 1e-9)):
                    ok = False
                    break
            if ok:
                continue
            return False
        return False
    
    return True

def build_visibility_graph(map_obj):
    graph = VisibilityGraph()
    all_vertices = [map_obj.q_start, map_obj.q_goal]
  
    for obstacle in map_obj.obstacles:
        obs_vertices = obstacle.vertices
        for i in range(len(obs_vertices)):
            v1 = obs_vertices[i]
            v2 = obs_vertices[(i + 1) % len(obs_vertices)]
            
            graph.add_vertex(v1)
            all_vertices.append(v1)
            
           
            distance = v1.distance_to(v2)
            graph.add_edge(v1, v2, distance)
    

    graph.add_vertex(map_obj.q_start)
    graph.add_vertex(map_obj.q_goal)
    
   
    unique_vertices = list(dict.fromkeys(all_vertices))    
    
    n = len(all_vertices)
    print(f"Verificando visibilidade entre {n} vértices...")
    
    edges_added = 0
    for i in range(n):
        for j in range(i + 1, n):
            v1, v2 = unique_vertices[i], unique_vertices[j]

            if v2 in graph.adj[v1]:
                continue
            
            if is_visible(v1, v2, map_obj.obstacles):
                distance = v1.distance_to(v2)
                graph.add_edge(v1, v2, distance)
                edges_added += 1
    
    print(f"Grafo criado com {n} vértices e {len(graph.get_edges())} arestas totais")
    return graph

if __name__ == "__main__":
    from Utils.file_reader import read_map_from_file
    from pathlib import Path
    
    project_root = Path(__file__).resolve().parent.parent
    map_path = project_root / "Mapa" / "map1.txt"
    
    if not map_path.is_file():
        print(f"Arquivo não encontrado: {map_path}")
    else:
        mapa = read_map_from_file(str(map_path))
        print(f"Mapa carregado: {mapa}")
        
        grafo = build_visibility_graph(mapa)
        print(f"\nTotal de vértices no grafo: {len(grafo.get_vertices())}")
        print(f"Total de arestas no grafo: {len(grafo.get_edges())}")