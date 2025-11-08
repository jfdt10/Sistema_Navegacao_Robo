class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.edges = []  # lista de (u,v,w)

    def add_edge(self, u, v, w):
        self.edges.append((u, v, w))

    def find(self, parent, i):
        if parent[i] != i:
            parent[i] = self.find(parent, parent[i])
        return parent[i]

    def union(self, parent, rank, x, y):
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1

    def kruskal_mst(self):
        result = []
        i = 0
        e = 0
        self.edges.sort(key=lambda item: item[2])
        parent = list(range(self.V))
        rank = [0] * self.V

        while e < self.V - 1 and i < len(self.edges):
            u, v, w = self.edges[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                result.append((u, v, w))
                self.union(parent, rank, x, y)
                e += 1

        total_cost = sum(w for _, _, w in result)
        return result, total_cost


if __name__ == '__main__':
    g = Graph(4)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 2, 6)
    g.add_edge(0, 3, 5)
    g.add_edge(1, 3, 15)
    g.add_edge(2, 3, 4)

    mst, cost = g.kruskal_mst()
    print("Edges in the constructed MST")
    for u, v, w in mst:
        print(f"{u} -- {v} == {w}")
    print("Minimum Spanning Tree", cost)