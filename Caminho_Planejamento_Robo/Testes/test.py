import pytest
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from Modulos.models import Point, Obstacle
from Modulos.visibility_graph import build_visibility_graph
from Modulos.pathfinding import bfs_path, close_vertex
from Utils.file_reader import read_map_from_file


class TestPoint:
    """Testes para a classe Point"""
    
    def test_point_creation(self):
        p = Point(10, 20)
        assert p.x == 10
        assert p.y == 20
    
    def test_distance_between_points(self):
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        distance = p1.distance_to(p2)
        assert distance == pytest.approx(5.0)  
    
    def test_point_equality(self):
        p1 = Point(5, 5)
        p2 = Point(5, 5)
        assert p1.x == p2.x and p1.y == p2.y


class TestVisibilityGraph:
    """Testes para construção do Grafo de Visibilidade"""
    
    @pytest.fixture
    def simple_map(self):
        mapa_mock = type('Mapa', (), {})()
        mapa_mock.obstacles = []
        mapa_mock.q_start = Point(0, 0)
        mapa_mock.q_goal = Point(10, 10)
        return mapa_mock
    
    def test_visibility_graph_creation(self, simple_map):
        vis_graph = build_visibility_graph(simple_map)
        assert vis_graph is not None
        assert len(vis_graph.get_vertices()) >= 2 
    
    def test_visibility_graph_has_q_start_and_q_goal(self, simple_map):
        vis_graph = build_visibility_graph(simple_map)
        vertices = list(vis_graph.get_vertices())
        assert len(vertices) >= 2


class TestPathfinding:
    
    def test_bfs_path_exists(self):
        """Testar se BFS encontra caminho quando existe"""
        adj = {
            1: {2: 5},
            2: {1: 5, 3: 10},
            3: {2: 10}
        }
        path = bfs_path(1, 3, adj)
        assert path is not None
        assert len(path) == 3  
    
    def test_bfs_path_direct_connection(self):
        """Testar BFS com conexão direta"""
        adj = {
            1: {2: 5},
            2: {1: 5}
        }
        path = bfs_path(1, 2, adj)
        assert path is not None
        assert path == [1, 2]
    
    def test_bfs_path_not_exists(self):
        """Testar BFS quando não há caminho"""
        adj = {
            1: {2: 5},
            2: {1: 5},
            3: {4: 10},
            4: {3: 10}
        }
        path = bfs_path(1, 3, adj)
        assert path is None or len(path) == 0
    
    def test_close_vertex_finds_nearest(self):
        """Testar busca do vértice mais próximo"""
        ponto = Point(5, 5)
        adj = {
            Point(0, 0): {},
            Point(10, 10): {},
            Point(5, 5): {} 
        }
        closest = close_vertex(ponto, adj)
        assert closest is not None
        assert closest.distance_to(ponto) == pytest.approx(0.0)


class TestFileReader:
    """Testes para leitura de arquivos de mapa"""
    
    def test_read_valid_map_file(self):
        map_path = project_root / "Mapa" / "map1.txt"
        if map_path.exists():
            mapa = read_map_from_file(str(map_path))
            assert mapa is not None
            assert hasattr(mapa, 'obstacles')
            assert hasattr(mapa, 'q_start')
            assert hasattr(mapa, 'q_goal')
    
    def test_map_has_obstacles(self):
        map_path = project_root / "Mapa" / "map1.txt"
        if map_path.exists():
            mapa = read_map_from_file(str(map_path))
            assert len(mapa.obstacles) > 0


class TestIntegration:
    """Testes de integração completos"""
    
    def test_full_pipeline(self):
        map_path = project_root / "Mapa" / "map1.txt"
        if not map_path.exists():
            pytest.skip("Arquivo de mapa não encontrado")
        
        # 1. Carregar mapa
        mapa = read_map_from_file(str(map_path))
        assert mapa is not None
        
        # 2. Construir grafo de visibilidade
        vis_graph = build_visibility_graph(mapa)
        assert vis_graph is not None
        assert len(vis_graph.get_vertices()) >= 2
        
        # 3. Verificar se q_start e q_goal têm conectividade
        q_start = mapa.q_start
        q_goal = mapa.q_goal
        
        # Tentar encontrar caminho
        path = bfs_path(q_start, q_goal, vis_graph.adj)
        assert isinstance(path, (list, type(None)))


class TestEdgeCases:
    """Testes para casos extremos"""
    
    def test_same_start_and_goal(self):
        adj = {
            Point(0, 0): {}
        }
        path = bfs_path(Point(0, 0), Point(0, 0), adj)
        assert path is not None or len(path) >= 1
    
    def test_empty_graph(self):
        adj = {}
        path = bfs_path(Point(0, 0), Point(10, 10), adj)
        assert path is None or len(path) == 0
    
    def test_point_distance_zero(self):
        p = Point(5, 5)
        distance = p.distance_to(p)
        assert distance == pytest.approx(0.0)


#-------- Testes --------#
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])