def floyd_warshall(graph):
    # получаем список всех вершин графа
    vertices = list(graph.keys())
    n = len(vertices)

    # инициализируем матрицы расстояний и предшественников
    dist = {v: {u: float('inf') for u in vertices} for v in vertices}
    next_v = {v: {u: None for u in vertices} for v in vertices}

    # заполняем матрицу расстояний начальными значениями из графа
    for v in vertices:
        for u in vertices:
            if u in graph[v]:
                dist[v][u] = graph[v][u]
                next_v[v][u] = u
            dist[v][v] = 0

    # выполняем основной алгоритм Флойда-Уоршелла
    for k in vertices:
        for i in vertices:
            for j in vertices:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_v[i][j] = next_v[i][k]

    return dist, next_v

def reconstruct_path(next_v, start, end):
    # восстанавливаем кратчайший путь от вершины start до вершины end
    path = []
    step = start
    while step is not None:
        path.append(step)
        if step == end:
            break
        step = next_v[step].get(end)
    return path

def calculate_path_weight(graph, path):
    # вычисляем вес пути, суммируя веса рёбер между последовательными вершинами в пути
    weight = 0
    for i in range(len(path) - 1):
        weight += graph[path[i]][path[i + 1]]
    return weight

def print_shortest_paths(graph, next_v, dist, vertices, target):
    # выводим кратчайшие пути до вершины target из всех остальных вершин
    for start in vertices:
        if start != target:
            path = reconstruct_path(next_v, start, target)
            weight = calculate_path_weight(graph, path)
            print(f"Shortest path from {start} to {target}: {path} with weight {weight}")

def read_graph_from_file(file_path):
    # считываем граф из файла и возвращаем его в виде словаря смежности
    graph = {}
    with open(file_path, 'r') as file:
        for line in file:
            start, end, weight = line.strip().split()
            weight = int(weight)
            if start not in graph:
                graph[start] = {}
            if end not in graph:
                graph[end] = {}
            graph[start][end] = weight
    return graph

graph = read_graph_from_file('input.txt')
dist, next_v = floyd_warshall(graph)
target_vertex = 'E'
print_shortest_paths(graph, next_v, dist, graph.keys(), target_vertex)
