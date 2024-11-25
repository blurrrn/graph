import heapq

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
            graph[end][start] = weight  # Если граф неориентированный
    return graph

def dijkstra(graph, start, end):
    queue = []
    heapq.heappush(queue, (0, start))

    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0

    predecessors = {vertex: None for vertex in graph}

    while queue:
        current_distance, current_vertex = heapq.heappop(queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_vertex
                heapq.heappush(queue, (distance, neighbor))

    path = []
    step = end
    while step is not None:
        path.append(step)
        step = predecessors[step]
    path = path[::-1]

    if distances[end] == float('infinity'):
        return "Путь не найден"
    else:
        return path, distances[end]

# Пример использования
file_path = 'graph.txt'  # Путь к файлу с графом
graph = read_graph_from_file(file_path)

start_vertex = 'A'
end_vertex = 'D'

path, distance = dijkstra(graph, start_vertex, end_vertex)
print(f"Кратчайший путь: {path}")
print(f"Длина пути: {distance}")
