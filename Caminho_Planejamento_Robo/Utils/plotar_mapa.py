import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
from pathlib import Path
from Utils.file_reader import read_map_from_file

def plot_map(map_obj, grafo=None, mst_graph=None, path=None, save_path=None, num_vertices=None, num_edges=None, cost=None, path_cost=None, algo_name=None):
    fig, ax = plt.subplots(figsize=(14, 11))
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
        for v1, v2, _ in grafo.get_edges():
            ax.plot([v1.x, v2.x], [v1.y, v2.y], c="#FF6F00", linewidth=1.8, alpha=0.8, zorder=2)

        for v in grafo.get_vertices():
            ax.scatter([v.x], [v.y], c="#FF6F00", s=60, marker='o', alpha=0.7, zorder=2.5, 
                      edgecolors='darkorange', linewidth=1.5)

    if mst_graph:
        for v1, v2, _ in mst_graph.get_edges():
            ax.plot([v1.x, v2.x], [v1.y, v2.y], c="#0F15CA", linewidth=3.5, alpha=1.0, zorder=3)
        
        for v in mst_graph.get_vertices():
            ax.scatter([v.x], [v.y], c="#0F15CA", s=80, marker='s', alpha=0.9, zorder=3.5, 
                      edgecolors='darkblue', linewidth=2)

    if path:
        if len(path) >= 2:
            xs = [p.x for p in path]
            ys = [p.y for p in path]
            ax.plot(xs, ys, c="#FF0000", linewidth=3.0, alpha=1.0, zorder=5, marker='D', markersize=8)
    
    ax.scatter([map_obj.q_start.x], [map_obj.q_start.y], c=point_color, s=200, zorder=6, 
               marker='*', edgecolors='darkred', linewidth=2)
    ax.scatter([map_obj.q_goal.x], [map_obj.q_goal.y], c=point_color, s=200, zorder=6, 
               marker='*', edgecolors='darkred', linewidth=2)

    verts = [v for obs in map_obj.obstacles for v in obs.vertices]
    all_pts = verts + [map_obj.q_start, map_obj.q_goal]
    xs = [v.x for v in all_pts]
    ys = [v.y for v in all_pts]
    
    if xs and ys:
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        dx = (xmax - xmin) if xmax != xmin else 1.0
        dy = (ymax - ymin) if ymax != ymin else 1.0
        offx = dx * 0.04
        offy = dy * 0.04
        
        ax.text(map_obj.q_start.x + offx, map_obj.q_start.y + offy, 'qstart',
                verticalalignment='bottom', horizontalalignment='left', zorder=7, fontsize=10, 
                fontweight='bold', color='darkred')
        ax.text(map_obj.q_goal.x - offx, map_obj.q_goal.y - offy, 'qgoal',
                verticalalignment='top', horizontalalignment='right', zorder=7, fontsize=10, 
                fontweight='bold', color='darkred')
        
        m = 0.08
        ax.set_xlim(xmin - dx*m, xmax + dx*m)
        ax.set_ylim(ymin - dy*m, ymax + dy*m)
    
    legend_elements = []
    if grafo:
        legend_elements.append(Line2D([0], [0], color="#FF6F00", linewidth=2.5, label='Grafo de Visibilidade', alpha=0.8))
    if mst_graph:
        algo_label = f'MST ({algo_name})' if algo_name else 'MST'
        legend_elements.append(Line2D([0], [0], color="#0F15CA", linewidth=3, label=algo_label, alpha=1.0))
    if path:
        legend_elements.append(Line2D([0], [0], color="#FF0000", linewidth=3, label='Caminho (BFS)', alpha=1.0))
    
    if legend_elements:
        ax.legend(handles=legend_elements, loc='lower left', fontsize=10, framealpha=0.92, 
                 edgecolor='black', fancybox=True, shadow=True)

    info_text = ""
    if grafo:
        info_text += f"GRAFO DE VISIBILIDADE:\n"
        info_text += f"  Vertices: {len(grafo.get_vertices())}\n"
        info_text += f"  Arestas: {len(grafo.get_edges())}\n"
    
    if mst_graph and num_vertices and num_edges and cost is not None:
        info_text += f"\nARVORE GERADORA MINIMA ({algo_name or 'MST'}):\n"
        info_text += f"  Vertices: {num_vertices}\n"
        info_text += f"  Arestas: {num_edges}\n"
        info_text += f"  Custo Total: {cost:.2f}\n"
    
    if path and path_cost is not None:
        info_text += f"\nCAMINHO (BFS):\n"
        info_text += f"  Vertices no Caminho: {len(path)}\n"
        info_text += f"  Custo do Caminho: {path_cost:.2f}\n"
    
    if info_text:
        fig.text(0.98, 0.97, info_text, fontsize=9, verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.95, pad=1.0, 
                         edgecolor='gray', linewidth=2),
                family='monospace', fontweight='bold')
    
    ax.invert_yaxis()  
    ax.axis('off')
    plt.tight_layout(pad=0.5)
    plt.subplots_adjust(right=0.72)

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight', pad_inches=0.25)
        print(f"Grafico salvo em {save_path}")
    
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
            print("Arquivo nao encontrado:", path)
        else:
            path = Path.cwd() / name
    
    mapa = read_map_from_file(str(path))
    plot_map(mapa, grafo=None, save_path="mapa_plotado.png")