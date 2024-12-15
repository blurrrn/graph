# input
# A B 1
# A C 4
# B C -3
# C D 2
# D A -1
def read_graph_from_file(file_path):
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

def bellman_ford_with_paths(graph, start):
    # инициализация расстояний и путей
    distance = {vertex: float('inf') for vertex in graph}
    distance[start] = 0
    paths = {vertex: [] for vertex in graph}
    paths[start] = [start]
    visited = set()

    # релаксация ребер
    for i in range(len(graph) - 1):
        for u in graph:
            for v in graph[u]:
                if distance[u] + graph[u][v] < distance[v] and [v] != [start]:
                    # if v in visited:
                    #   break
                    # else:
                    #   visited.add(v)
                    distance[v] = distance[u] + graph[u][v]
                    paths[v] = paths[u] + [v]

    # проверка наличия циклов отрицательного веса
    for u in graph:
        for v in graph[u]:
            if distance[u] + graph[u][v] < distance[v]:
                break

    return distance, paths

def all_pairs_shortest_paths(graph):
    all_distances = {}
    all_paths = {}
    for start in graph:
        distances, paths = bellman_ford_with_paths(graph, start)
        if distances is not None:
            all_distances[start] = distances
            all_paths[start] = paths
    return all_distances, all_paths

def print_shortest_paths(all_distances, all_paths):
    for start in all_distances:
        print(f"Кратчайшие пути из вершины {start}:")
        for end in all_distances[start]:
            print(f"  В вершину {end}: {all_distances[start][end]}")
            print(f"  Путь: {all_paths[start][end]}")
        print()

graph = read_graph_from_file('input.txt')
all_distances, all_paths = all_pairs_shortest_paths(graph)
print_shortest_paths(all_distances, all_paths)
