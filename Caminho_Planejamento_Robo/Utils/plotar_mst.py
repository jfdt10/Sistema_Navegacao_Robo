from pathlib import Path
from Utils.file_reader import read_map_from_file
from Modulos.visibility_graph import build_visibility_graph, VisibilityGraph
from Modulos.kruskal import Graph as KruskalGraph
from Modulos import prim as prim_mod
from Utils.plotar_mapa import plot_map

def build_mst_from_visibility(mapa, algorithm="kruskal"):
 
    vis = build_visibility_graph(mapa)

    if algorithm.lower() == "kruskal":
        verts = vis.get_vertices()
        idx_of = {v: i for i, v in enumerate(verts)}
        n = len(verts)

        kg = KruskalGraph(n)
        for a, b, w in vis.get_edges():
            ua, ub = idx_of[a], idx_of[b]
            kg.add_edge(ua, ub, w)

        mst_idx_edges, total_cost = kg.kruskal_mst()

        mst_graph = VisibilityGraph()
        for u_idx, v_idx, w in mst_idx_edges:
            a = verts[u_idx]
            b = verts[v_idx]
            mst_graph.add_edge(a, b, w)

        return vis, mst_graph, total_cost, "Kruskal"

    elif algorithm.lower() == "prim":
        mst_edges = prim_mod.prim_mst(vis)
        total_cost = sum(w for _, _, w in mst_edges)
        mst_graph = VisibilityGraph()
        for v1, v2, w in mst_edges:
            mst_graph.add_edge(v1, v2, w)
        return vis, mst_graph, total_cost, "Prim"

    else:
        raise ValueError("Algoritmo deve ser 'kruskal' ou 'prim'")

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    map_path = project_root / "Mapa" / "map1.txt"
    if not map_path.is_file():
        print("Arquivo map1.txt não encontrado em:", map_path)
    else:
        mapa = read_map_from_file(str(map_path))

        grafo, mst_graph, cost, algo_name = build_mst_from_visibility(mapa, algorithm="prim")

        num_vertices = len(mst_graph.get_vertices())
        num_edges = len(mst_graph.get_edges())

        print(f"\n MST gerada com {algo_name}!")
        print(f"Vertices na MST: {num_vertices}")
        print(f"Arestas na MST: {num_edges}")
        print(f"Custo total (distância): {cost}")
        print(f"MST é árvore (E == V-1): {num_edges == max(0, num_vertices-1)}")

        plot_map(mapa, grafo=grafo, mst_graph=mst_graph, save_path="mapa_mst_prim.png")
        print(f"Gráfico salvo em mapa_mst_prim.png")