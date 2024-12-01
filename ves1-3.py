import heapq

#чтение графа из файла
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
            graph[end][start] = weight
    return graph

#алгоритм Дейкстры для нахождения кратчайшего пути из вершины u до вершины v
def dijkstra(graph, start, end):
    #инициализация очереди с приоритетом и расстояний
    queue = [(0, start)]
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    previous_vertices = {vertex: None for vertex in graph}

    while queue:
        current_distance, current_vertex = heapq.heappop(queue)

        #если текущее расстояние больше сохраненного, пропускаем
        if current_distance > distances[current_vertex]:
            continue

        #обновление расстояний до соседних вершин
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(queue, (distance, neighbor))

    #восстановление пути
    path, current_vertex = [], end
    while previous_vertices[current_vertex] is not None:
        path.insert(0, current_vertex)
        current_vertex = previous_vertices[current_vertex]
    if path:
        path.insert(0, current_vertex)
    return distances[end], path

#алгоритм Беллмана-Форда для нахождения кратчайших путей до вершины u из всех остальных вершин
def bellman_ford(graph, start):
    #инициализация расстояний и предыдущих вершин
    distance = {vertex: float('infinity') for vertex in graph}
    distance[start] = 0
    previous_vertices = {vertex: None for vertex in graph}

    #релаксация ребер
    for _ in range(len(graph) - 1):
        for u in graph:
            for v, weight in graph[u].items():
                if distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight
                    previous_vertices[v] = u

    return distance, previous_vertices

#алгоритм Флойда-Уоршелла для нахождения кратчайших путей для всех пар вершин
def floyd_warshall(graph):
    vertices = list(graph.keys())
    distance = {vertex: {v: float('infinity') for v in vertices} for vertex in vertices}
    next_vertex = {vertex: {v: None for v in vertices} for vertex in vertices}

    #инициализация матрицы расстояний
    for u in graph:
        distance[u][u] = 0
        for v, weight in graph[u].items():
            distance[u][v] = weight
            next_vertex[u][v] = v

    #обновление матрицы расстояний
    for k in vertices:
        for i in vertices:
            for j in vertices:
                if distance[i][j] > distance[i][k] + distance[k][j]:
                    distance[i][j] = distance[i][k] + distance[k][j]
                    next_vertex[i][j] = next_vertex[i][k]

    return distance, next_vertex

graph = read_graph_from_file('input.txt')

#задача 1: Кратчайший путь из вершины u до вершины v
start_vertex = input('Введите началбную вершину: ')
end_vertex = input('Введите конечную вершину: ')
distance, path = dijkstra(graph, start_vertex, end_vertex)
print(f"Кратчайший путь из {start_vertex} до {end_vertex}: {path}")
print(f"Длина пути: {distance}\n")

#задача 2: Кратчайшие пути до вершины u из всех остальных вершин
start_vertex = input('Введите началбную вершину: ')
distances, previous_vertices = bellman_ford(graph, start_vertex)
print(f"Кратчайшие пути до вершины {start_vertex}: {distances}\n")

#задача 3: Кратчайшие пути для всех пар вершин
distances, next_vertices = floyd_warshall(graph)
print("Кратчайшие пути для всех пар вершин:")
for start in distances:
    for end in distances[start]:
        print(f"Кратчайший путь из {start} до {end}: {distances[start][end]}")
