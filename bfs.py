def read_graph_from_file(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 1:
                node = parts[0]
                if node not in graph:
                    graph[node] = []
            elif len(parts) > 1:
                node = parts[0]
                neighbors = parts[1:]
                if node not in graph:
                    graph[node] = []
                graph[node].extend(neighbors)
                for neighbor in neighbors:
                    if neighbor not in graph:
                        graph[neighbor] = []
                    if node not in graph[neighbor]:
                        graph[neighbor].append(node)
    return graph

def bfs(graph, start):
    visited = set()
    queue = [(start, 0)]
    max_distance = 0

    while queue:
        vertex, distance = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            max_distance = max(max_distance, distance)
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    queue.append((neighbor, distance + 1))

    return max_distance

def find_radius(graph):
    eccentricities = []
    for vertex in graph:
        eccentricities.append(bfs(graph, vertex))
    return min(eccentricities)

graph = read_graph_from_file('input.txt')
radius = find_radius(graph)
print(f"Радиус графа: {radius}")
