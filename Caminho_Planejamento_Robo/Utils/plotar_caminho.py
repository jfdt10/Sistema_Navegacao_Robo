from pathlib import Path
from Utils.file_reader import read_map_from_file
from Utils.plotar_mst import build_mst_from_visibility
from Utils.plotar_mapa import plot_map
from Modulos.pathfinding import bfs_path

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

        print(f"\nMST gerada com {algo_name}!")
        print(f"Vertices na MST: {num_vertices}")
        print(f"Arestas na MST: {num_edges}")
        print(f"Custo total MST: {cost:.2f}")

        path = bfs_path(mapa.q_start, mapa.q_goal, mst_graph.adj)

        if path:
            path_cost = sum(mst_graph.adj[path[i]][path[i+1]] for i in range(len(path)-1))
            print(f" Caminho encontrado!")
            print(f"Vertices no caminho: {len(path)}")
            print(f"Custo do caminho: {path_cost:.2f}")
        else:
            print("Nenhum caminho encontrado entre q_start e q_goal")

        plot_map(mapa, grafo=grafo, mst_graph=mst_graph, path=path, save_path="mapa_caminho.png")
        print(f"Gráfico salvo em mapa_caminho.png")