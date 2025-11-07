import numpy as np
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry import Polygon as ShapelyPolygon


class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9
    
    def __hash__(self):
        return hash((round(self.x, 6), round(self.y, 6)))
    
    def __repr__(self):
        return f"Point({self.x:.2f}, {self.y:.2f})"
    
    def distance_to(self, other):
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def to_tuple(self):
        return (self.x, self.y)


class Obstacle:
    def __init__(self, vertices):
        if vertices and isinstance(vertices[0], Point):
            self.vertices = vertices
        else:
            self.vertices = [Point(v[0], v[1]) for v in vertices]
        
        coords = [(v.x, v.y) for v in self.vertices]
        self.shapely_polygon = ShapelyPolygon(coords)
    
    def get_edges(self):
        edges = []
        n = len(self.vertices)
        for i in range(n):
            edges.append((self.vertices[i], self.vertices[(i+1) % n]))
        return edges
    
    def contains_point(self, point):
        shapely_point = ShapelyPoint(point.x, point.y)
        return self.shapely_polygon.contains(shapely_point)
    
    def __repr__(self):
        return f"Obstacle({len(self.vertices)} vertices)"
    
class Map:
    def __init__(self, q_start: Point, q_goal: Point, obstacles: list):
        self.q_start = q_start
        self.q_goal = q_goal
        self.obstacles = obstacles
    
    @property
    def all_vertices(self):
        obstacle_vertices = []
        for obs in self.obstacles:
            obstacle_vertices.extend(obs.vertices)
        return [self.q_start] + obstacle_vertices + [self.q_goal]
    
    def __repr__(self):
        return f"Map(start={self.q_start}, goal={self.q_goal}, {len(self.obstacles)} obstacles)"



if __name__ == "__main__":
    print("Testando models.py...\n")
    
    # Teste Point
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    print(f"Distância: {p1.distance_to(p2):.2f}")  # 5.00
    
    # Teste Obstacle
    quadrado = Obstacle([[0, 0], [10, 0], [10, 10], [0, 10]])
    print(f"Point(5,5) dentro? {quadrado.contains_point(Point(5, 5))}")   # True
    print(f"Point(15,15) dentro? {quadrado.contains_point(Point(15, 15))}")  # False
    
    # Teste Map
    mapa_teste = Map(p1, p2, [quadrado])
    print(f"\nObjeto Mapa: {mapa_teste}")
    print(f"Todos os vértices do mapa: {mapa_teste.all_vertices}")