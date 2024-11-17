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

def dfs(graph, start, end, path, paths):
    path.append(start)
    if start == end:
        paths.append(path.copy())
    else:
        for neighbor in graph[start]:
            if neighbor not in path:
                dfs(graph, neighbor, end, path, paths)
    path.pop()

def find_all_paths(graph, start, end):
    paths = []
    dfs(graph, start, end, [], paths)
    return paths

graph = read_graph_from_file('input.txt')

if graph is not None:
    start_vertex = input("Введите начальную вершину: ")
    end_vertex = input("Введите конечную вершину: ")

    if start_vertex not in graph:
        print(f"Начальная вершина {start_vertex} не найдена в графе.")
    elif end_vertex not in graph:
        print(f"Конечная вершина {end_vertex} не найдена в графе.")
    else:
        all_paths = find_all_paths(graph, start_vertex, end_vertex)
        if all_paths:
            for path in all_paths:
                print(" -> ".join(path))
        else:
            print("Пути между вершинами не найдены.")
else:
    print("Не удалось загрузить граф.")
