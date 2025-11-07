from pathlib import Path
from Utils.file_reader import read_map_from_file
from Modulos.visibility_graph import build_visibility_graph
from Utils.plotar_mapa import plot_map

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    maps_dir = project_root / "Mapa"
    map_path = maps_dir / "map1.txt"

    if not map_path.is_file():
        print("Arquivo não encontrado:", map_path)
    else:
        mapa = read_map_from_file(str(map_path))
        grafo = build_visibility_graph(mapa)
        plot_map(mapa, grafo=grafo, save_path="mapa_visibilidade.png")