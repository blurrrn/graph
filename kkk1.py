def kruskal(edges, num_vertices):
    # Сортируем ребра по весу
    edges = sorted(edges, key=lambda item: item[2])

    # Инициализируем родительские узлы и ранги
    parent = list(range(num_vertices))
    rank = [0] * num_vertices

    mst = []
    i = 0
    e = 0

    while e < num_vertices - 1:
        u, v, w = edges[i]
        i += 1

        # Находим корни узлов u и v
        x = u
        while parent[x] != x:
            x = parent[x]

        y = v
        while parent[y] != y:
            y = parent[y]

        # Если корни разные, объединяем их
        if x != y:
            e += 1
            mst.append([u, v, w])

            # Объединяем множества
            if rank[x] < rank[y]:
                parent[x] = y
            elif rank[x] > rank[y]:
                parent[y] = x
            else:
                parent[y] = x
                rank[x] += 1

    return mst

def read_graph_from_file(file_path):
    with open(file_path, 'r') as file:
        num_vertices = int(file.readline().strip())
        num_edges = int(file.readline().strip())
        edges = []
        for _ in range(num_edges):
            u, v, w = map(int, file.readline().strip().split())
            edges.append([u, v, w])
    return num_vertices, edges

def main():
    file_path = 'graph.txt'  # Замените на путь к вашему файлу
    num_vertices, edges = read_graph_from_file(file_path)
    mst = kruskal(edges, num_vertices)

    print("Ребра минимального остовного дерева:")
    for u, v, weight in mst:
        print(f"{u} -- {v} == {weight}")

if __name__ == "__main__":
    main()
