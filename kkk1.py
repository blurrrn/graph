def find(parent, u):
    if parent[u] != u:
        parent[u] = find(parent, parent[u])
    return parent[u]

def union(parent, rank, u, v):
    root_u = find(parent, u)
    root_v = find(parent, v)
    if root_u != root_v:
        if rank[root_u] > rank[root_v]:
            parent[root_v] = root_u
        elif rank[root_u] < rank[root_v]:
            parent[root_u] = root_v
        else:
            parent[root_v] = root_u
            rank[root_u] += 1

def kruskal(n, edges):
    edges.sort(key=lambda x: x[2])  # Сортируем ребра по весу
    parent = list(range(n))
    rank = [0] * n
    mst = []
    mst_weight = 0

    for u, v, w in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst.append((u, v, w))
            mst_weight += w

    return mst, mst_weight

def read_graph_from_file(file_path):
    with open(file_path, 'r') as file:
        n, m = map(int, file.readline().split())
        edges = []
        for _ in range(m):
            u, v, w = map(int, file.readline().split())
            edges.append((u, v, w))
    return n, edges

# Пример использования
file_path = 'graph.txt'  # Путь к файлу с графом
N, edges = read_graph_from_file(file_path)
mst, mst_weight = kruskal(N, edges)
print("Ребра минимального остовного дерева:", mst)
print("Вес минимального остовного дерева:", mst_weight)
