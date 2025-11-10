from pathlib import Path
from Modulos.models import Point
from Modulos.visibility_graph import build_visibility_graph
from Modulos.pathfinding import bfs_path,close_vertex
from Utils.plotar_mapa import plot_map
from Utils.file_reader import read_map_from_file
from Utils.plotar_mst import build_mst_from_visibility

def print_main_menu():
    print("\n" + "="*70)
    print("SISTEMA DE NAVEGACAO PARA ROBOS AUTONOMOS")
    print("="*70)
    print("1. Carregar mapa e construir Grafo de Visibilidade")
    print("2. Construir Arvore Geradora Minima (MST)")
    print("3. Buscar caminho na MST")
    print("4. Encontrar vertice mais proximo na Árvore Geradora Minima (MST)")
    print("5. Plotar resultado final (unificado)")
    print("6. Limpar dados")
    print("7. Sair")
    print("="*70)

def print_mst_menu():
    print("\nEscolha o algoritmo para MST:")
    print("1. Kruskal")
    print("2. Prim")
    print("3. Voltar")

def print_custom_points_menu():
    print("\nOpcoes de pontos q_start e q_goal:")
    print("1. Usar pontos do arquivo (padrao)")
    print("2. Definir pontos customizados")
    print("3. Voltar")

def print_plot_menu():
    print("\nOpcoes de visualizacao:")
    print("1. Plotar Grafo de Visibilidade")
    print("2. Plotar MST")
    print("3. Plotar Caminho")
    print("4. Plotar tudo unificado")
    print("5. Voltar")
    
def print_exit_message():
    print("\nObrigado por usar o Sistema de Navegação para Robôs Autônomos. Até logo!")


def mst_selection(mapa):
     while True:
        print_mst_menu()
        choice = input("Escolha (1-3): ").strip()
        
        if choice == "1":
            print("\nConstruindo MST com Kruskal...")
            vis, mst_graph, cost, algo_name = build_mst_from_visibility(mapa, algorithm="kruskal")
            print(f"MST construida com sucesso!")
            print(f"  Vertices: {len(mst_graph.get_vertices())}")
            print(f"  Arestas: {len(mst_graph.get_edges())}")
            print(f"  Custo total: {cost:.2f}")
            return mst_graph, cost, "Kruskal", vis
        
        elif choice == "2":
            print("\nConstruindo  MST com Prim...")
            vis, mst_graph, cost, algo_name = build_mst_from_visibility(mapa, algorithm="prim")
            print(f"MST construida com sucesso!")
            print(f"  Vertices: {len(mst_graph.get_vertices())}")
            print(f"  Arestas: {len(mst_graph.get_edges())}")
            print(f"  Custo total: {cost:.2f}")
            return mst_graph, cost, "Prim", vis
        
        elif choice == "3":
            return None, None, None, None
        else:
            print("Opcao invalida!")

def map_selection():
    project_root = Path(__file__).resolve().parent
    maps_dir = project_root / "Mapa"

    map_files = list(maps_dir.glob("*.txt"))
    
    if not map_files:
        print("Nenhum arquivo de mapa encontrado na pasta Mapa/")
        return None
    
    print("\nArquivos de mapa disponíveis:")
    for i, f in enumerate(map_files, 1):
        print(f"{i}. {f.name}")
    
    try:
        choice = int(input("Escolha um arquivo (numero): ").strip())
        if 1 <= choice <= len(map_files):
            return map_files[choice - 1]
        else:
            print("Opcao invalida!")
            return None
    except ValueError:
        print("Entrada invalida!")
        return None


def custom_points(mapa, vis_graph):
 while True:
        print_custom_points_menu()
        choice = input("Escolha (1-3): ").strip()
        
        if choice == "1":
            print(f"Usando pontos do arquivo:")
            print(f"  q_start: ({mapa.q_start.x}, {mapa.q_start.y})")
            print(f"  q_goal: ({mapa.q_goal.x}, {mapa.q_goal.y})")
            return mapa.q_start, mapa.q_goal
        
        elif choice == "2":
            if vis_graph:
                vertices = list(vis_graph.get_vertices())
                print("\nSugestoes de coordenadas (vertices do grafo):")
                for i, v in enumerate(vertices[:8], 1): 
                    print(f"  {i}. ({v.x:.1f}, {v.y:.1f})")
                if len(vertices) > 8:
                    print(f"  ... e mais {len(vertices)-8} vertices")
            
            try:
                print("\nDigite as coordenadas:")
                x1 = float(input("q_start X: "))
                y1 = float(input("q_start Y: "))
                x2 = float(input("q_goal X: "))
                y2 = float(input("q_goal Y: "))
                
                q_start = Point(x1, y1)
                q_goal = Point(x2, y2)
                
                verts = [v for obs in mapa.obstacles for v in obs.vertices]
                if verts:
                    xs = [v.x for v in verts]
                    ys = [v.y for v in verts]
                    xmin, xmax = min(xs), max(xs)
                    ymin, ymax = min(ys), max(ys)
                    
                    if not (xmin <= q_start.x <= xmax and ymin <= q_start.y <= ymax):
                        print(f"Aviso: q_start está fora do mapa (x:[{xmin:.1f},{xmax:.1f}], y:[{ymin:.1f},{ymax:.1f}])")
                    if not (xmin <= q_goal.x <= xmax and ymin <= q_goal.y <= ymax):
                        print(f"Aviso: q_goal está fora do mapa (x:[{xmin:.1f},{xmax:.1f}], y:[{ymin:.1f},{ymax:.1f}])")
                
                print(f"Pontos customizados:")
                print(f"  q_start: ({q_start.x}, {q_start.y})")
                print(f"  q_goal: ({q_goal.x}, {q_goal.y})")
                return q_start, q_goal
                
            except ValueError:
                print("Entrada invalida! Tente novamente.")
        
        elif choice == "3":
            print("Voltando ao menu principal...")
            return None, None
        
        else:
            print("Opcao invalida! Use 1, 2 ou 3.")

def find_closest_vertex(mst_graph):
    try:
        print("\nDigite as coordenadas do ponto (no formato: x y)")
        x = float(input("Digite a coordenada X do ponto: "))
        y = float(input("Digite a coordenada Y do ponto: "))
        ponto = Point(x, y)

        closest = close_vertex(ponto, mst_graph.adj)
        if closest:
            dist = ponto.distance_to(closest)
            print(f"Vertice mais proximo encontrado:")
            print(f"  Coordenadas: ({closest.x}, {closest.y})")
            print(f"  Distancia: {dist:.2f}")
        else:
            print("Erro ao encontrar vertice mais proximo!")
    except ValueError:
        print("Entrada invalida!")

def plot_options(mapa, vis_graph, mst_graph, mst_cost, mst_algorithm, path, path_cost):
    while True:
        print_plot_menu()
        choice = input("Escolha (1-5): ").strip()
        
        if choice == "1":
            if vis_graph is None:
                print("Carregue o mapa primeiro!")
                continue
            print("Plotando Grafo de Visibilidade...")
            plot_map(mapa, grafo=vis_graph, save_path=f"01_visibilidade.png",num_vertices=len(vis_graph.get_vertices()),num_edges=len(vis_graph.get_edges()))
        
        elif choice == "2":
            if mst_graph is None:
                print("Construa uma MST primeiro!")
                continue
            print("Plotando MST...")
            plot_map(mapa, grafo=None, mst_graph=mst_graph, save_path=f"02_mst_{mst_algorithm.lower()}.png",num_vertices=len(mst_graph.get_vertices()),num_edges=len(mst_graph.get_edges()),cost=mst_cost,algo_name=mst_algorithm)

        elif choice == "3":
            if path is None:
                print("Busque um caminho primeiro!")
                continue
            print("Plotando Caminho...")
            plot_map(mapa, grafo=None, mst_graph=mst_graph, path=path, save_path=f"03_caminho_{mst_algorithm.lower()}.png",num_vertices=len(mst_graph.get_vertices()),num_edges=len(mst_graph.get_edges()),cost=mst_cost,path_cost=path_cost,algo_name=mst_algorithm)

        elif choice == "4":
            if vis_graph is None:
                print("Carregue o mapa primeiro!")
                continue
            print("Plotando tudo unificado...")
            plot_map(mapa,grafo=vis_graph,mst_graph=mst_graph,path=path,save_path=f"04_resultado_unificado_{mst_algorithm.lower()}.png",num_vertices=len(mst_graph.get_vertices()),num_edges=len(mst_graph.get_edges()),cost=mst_cost,path_cost=path_cost,algo_name=mst_algorithm)

        elif choice == "5":
            break
        else:
            print("Opcao invalida!")

def print_summary(vis_graph, mst_graph, mst_cost, mst_algorithm, path, path_cost):
    print("\n" + "="*70)
    print("RESUMO DOS DADOS ATUAIS")
    print("="*70)

    if vis_graph:
        print(f"Grafo de Visibilidade:")
        print(f"  Vertices: {len(vis_graph.get_vertices())}")
        print(f"  Arestas: {len(vis_graph.get_edges())}")
    else:
        print("Grafo de Visibilidade: Nao carregado")

    if mst_graph:
        print(f"\nArvore Geradora Minima ({mst_algorithm}):")
        print(f"  Vertices: {len(mst_graph.get_vertices())}")
        print(f"  Arestas: {len(mst_graph.get_edges())}")
        print(f"  Custo total: {mst_cost:.2f}")
    else:
        print("\nArvore Geradora Minima: Nao construida")
    
    if path:
        print(f"\nCaminho:")
        print(f"  Vertices no caminho: {len(path)}")
        print(f"  Custo: {path_cost:.2f}")
    else:
        print("\nCaminho: Nao encontrado")
    
    print("="*70)


def main():
    
    mapa = None
    vis_graph = None
    mst_graph = None
    mst_cost = None
    mst_algorithm = None
    path = None
    path_cost = None
    q_start = None
    q_goal = None

    while True:
        print_main_menu()
        op = input("Escolha uma opção (1-7): ").strip()

        if op == '1':
            print("\nCarregando mapa...")
            
            map_path = map_selection()
            if map_path is None:
                continue
            
            mapa = read_map_from_file(str(map_path))
            
            print(f"\nPontos padrão do arquivo:")
            print(f"  q_start: ({mapa.q_start.x}, {mapa.q_start.y})")
            print(f"  q_goal: ({mapa.q_goal.x}, {mapa.q_goal.y})")
            
            vis_graph_temp = build_visibility_graph(mapa)
            
            q_start, q_goal = custom_points(mapa, vis_graph_temp)
            
            if q_start is None or q_goal is None:
                print("Operacao cancelada. Voltando ao menu principal...")
                continue
            
            mapa.q_start = q_start
            mapa.q_goal = q_goal
            
            print("\nConstruindo Grafo de Visibilidade com os pontos escolhidos...")
            vis_graph = build_visibility_graph(mapa)
            
            print(f"Grafo construído com sucesso!")
            print(f"  Vertices: {len(vis_graph.get_vertices())}")
            print(f"  Arestas: {len(vis_graph.get_edges())}")
            
            print("\nPlotando Grafo de Visibilidade...")
            plot_map(mapa, grafo=vis_graph, save_path="01_visibilidade.png",num_vertices=len(vis_graph.get_vertices()),num_edges=len(vis_graph.get_edges()))

        elif op == '2':
            if vis_graph is None:
                print("Carregue o mapa primeiro!")
                continue

            mst_graph, mst_cost, mst_algorithm, vis_graph_updated = mst_selection(mapa)

            if mst_graph is None:
                print("Operacao cancelada.")
                continue

            if vis_graph_updated is not None:
                vis_graph = vis_graph_updated

            print("\nPlotando MST...")
            plot_map(mapa, grafo=None, mst_graph=mst_graph, save_path=f"02_mst_{mst_algorithm.lower()}.png", num_vertices=len(mst_graph.get_vertices()), num_edges=len(mst_graph.get_edges()), cost=mst_cost, algo_name=mst_algorithm)
        
        elif op == '3':
            if mst_graph is None:
                print("Construa uma MST primeiro (opcao 2)!")
                continue
            
            print(f"\nBuscando caminho na MST...")
            path = bfs_path(q_start, q_goal, mst_graph.adj)
            
            if path:
                path_cost = sum(mst_graph.adj[path[i]][path[i+1]] for i in range(len(path)-1))
                print(f"Caminho encontrado com sucesso!")
                print(f"  Vertices no caminho: {len(path)}")
                print(f"  Custo: {path_cost:.2f}")
            
                print("\n Plotando Caminho...")
                plot_map(mapa, grafo=None, mst_graph=mst_graph, path=path, save_path="03_caminho.png",num_vertices=len(mst_graph.get_vertices()),num_edges=len(mst_graph.get_edges()),cost=mst_cost,path_cost=path_cost,algo_name=mst_algorithm)

            else:
                print("Nenhum caminho encontrado entre q_start e q_goal")
                path = None
                path_cost = None

        elif op == '4':
            if mst_graph is None:
                print("Carregue o mapa primeiro!")
                continue
            find_closest_vertex(mst_graph)

        elif op == '5':
            if vis_graph is None or mst_graph is None:
                print("Carregue o mapa e construa a MST primeiro!")
                continue
            plot_options(mapa, vis_graph, mst_graph, mst_cost, mst_algorithm, path, path_cost)

        elif op == '6':
            mapa = None
            vis_graph = None
            mst_graph = None
            mst_cost = None
            mst_algorithm = None
            path = None
            path_cost = None
            q_start = None
            q_goal = None
            print("Dados limpos com sucesso!")

        elif op == '7':
            print_exit_message()
            break

        else:
            print("Opcao invalida! Escolha entre 1 e 7.")
        
        if op in ["1", "2", "3"]:
            print_summary(vis_graph, mst_graph, mst_cost, mst_algorithm, path, path_cost)

if __name__ == "__main__":
    main()
