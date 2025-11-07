import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path
from Utils.file_reader import read_map_from_file

def plot_map(map_obj, grafo=None, save_path=None):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    obstacle_color = '#4d4d4d'  
    point_color = '#ff0000'     

    for obs in map_obj.obstacles:
        try:
            coords = [(v.x, v.y) for v in obs.vertices]
            ax.add_patch(Polygon(coords, closed=True, facecolor=obstacle_color, edgecolor=None, zorder=1))
        except Exception:
            continue
    
    if grafo:
        for v1,v2,_ in grafo.get_edges():
            ax.plot([v1.x, v2.x], [v1.y, v2.y], c="#FF6F00", linewidth=0.8, alpha=1.0, zorder=2)

    ax.scatter([map_obj.q_start.x], [map_obj.q_start.y], c=point_color, s=60, zorder=4)
    ax.scatter([map_obj.q_goal.x], [map_obj.q_goal.y], c=point_color, s=60, zorder=4)

    verts = [v for obs in map_obj.obstacles for v in obs.vertices]
    all_pts = verts + [map_obj.q_start, map_obj.q_goal]
    xs = [v.x for v in all_pts]
    ys = [v.y for v in all_pts]
    
    if xs and ys:
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        dx = (xmax - xmin) if xmax != xmin else 1.0
        dy = (ymax - ymin) if ymax != ymin else 1.0
        offx = dx * 0.02
        offy = dy * 0.02
        
        ax.text(map_obj.q_start.x + offx, map_obj.q_start.y + offy, 'qstart',
                verticalalignment='bottom', horizontalalignment='left', zorder=5)
        ax.text(map_obj.q_goal.x - offx, map_obj.q_goal.y - offy, 'qgoal',
                verticalalignment='top', horizontalalignment='right', zorder=5)
        
        
        m = 0.05
        ax.set_xlim(xmin - dx*m, xmax + dx*m)
        ax.set_ylim(ymin - dy*m, ymax + dy*m)

    ax.invert_yaxis()  
    ax.axis('off')
    plt.tight_layout(pad=0)

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight', pad_inches=0.1)
    
    plt.show()
    plt.close(fig)


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    maps_dir = project_root / "Mapa"
    name = "map1.txt"
    candidate = Path(name)
    if candidate.parent == Path('.') and not candidate.is_absolute():
        path = maps_dir / candidate.name
    else:
        path = candidate

    if not path.is_file():
        if not (Path.cwd() / name).is_file():
            print("Arquivo não encontrado:", path)
        else:
            path = Path.cwd() / name
    
    mapa = read_map_from_file(str(path))
    plot_map(mapa, grafo=None, save_path="mapa_plotado.png")