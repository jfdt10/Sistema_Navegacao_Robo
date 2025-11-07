from Modulos.models import Point, Obstacle, Map
from pathlib import Path

def _parser_coords(coord_str:str):
    parts = [p.strip() for p in coord_str.split(',') if p.strip() != '']
    if len(parts) < 2:
        raise ValueError(f"Coordenadas inválidas: '{coord_str}'")
    x,y = float(parts[0]), float(parts[1])
    return Point(x, y)

def read_map_from_file(file_path:str):
    with open(file_path, 'r') as f:
        raw_lines = [ln.strip() for ln in f.readlines()]
        lines = [ln for ln in raw_lines if ln and not ln.startswith('#')]

    line_idx = 0

    try:
        q_start = _parser_coords(lines[line_idx])
        line_idx += 1
        q_goal = _parser_coords(lines[line_idx])
        line_idx += 1

        num_obstacles = int(lines[line_idx])
        line_idx += 1
        obstacles = []
        for i in range(num_obstacles):
            num_vertices = int(lines[line_idx])
            line_idx += 1
            vertices = []
            for i in range(num_vertices):
                vertex = _parser_coords(lines[line_idx])
                vertices.append(vertex)
                line_idx += 1
            obstacles.append(Obstacle(vertices))
        return Map(q_start, q_goal, obstacles)
    except IndexError:
        raise ValueError("Arquivo de mapa truncado ou formato incorreto.")
    except ValueError as e:
        raise ValueError(f"Erro ao parsear arquivo de mapa: {e}")



if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    fixed_maps_dir = project_root / "Mapa"

    nome = input("Nome do arquivo de mapa (ex: map1.txt): ").strip()
    candidate = Path(nome)

    if candidate.parent == Path('.') and not candidate.is_absolute():
        map_path = fixed_maps_dir / candidate.name
    else:
        map_path = candidate

    if not map_path.is_file():
        print(f"Arquivo não encontrado: {map_path}")
        print(f"Coloque '{candidate.name}' em: {fixed_maps_dir} ou informe caminho completo.")
    else:
        mapa = read_map_from_file(str(map_path))
        print("Mapa carregado:")
        print(mapa)
        print("Vértices:", mapa.all_vertices)