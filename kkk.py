class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

def kruskal(n, edges):
    edges.sort(key=lambda x: x[2])  # сортируем ребра по весу
    dsu = DSU(n)
    mst = []
    mst_weight = 0

    for u, v, w in edges:
        if dsu.find(u) != dsu.find(v):
            dsu.union(u, v)
            mst.append((u, v, w))
            mst_weight += w

    return mst, mst_weight

N = 4
M = 5
edges = [
    (0, 1, 1),
    (0, 2, 3),
    (1, 2, 3),
    (1, 3, 4),
    (2, 3, 2)
]

mst, mst_weight = kruskal(N, edges)
print("Ребра минимального остовного дерева:", mst)
print("Вес минимального остовного дерева:", mst_weight)
