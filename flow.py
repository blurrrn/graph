# A B 16
# A C 13
# B C 10
# B D 12
# C E 14
# D B 9
# D F 20
# E D 7
# E F 4

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

def bfs(graph, source, sink, parent):
    visited = {source}
    queue = [source]

    while queue:
        u = queue.pop(0)

        for v, capacity in graph[u].items():
            if v not in visited and capacity > 0:
                queue.append(v)
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return True
    return False

def ford_fulkerson(graph, source, sink):
    parent = {}
    max_flow = 0

    while bfs(graph, source, sink, parent):
        path_flow = float('Inf')
        s = sink

        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        max_flow += path_flow

        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            if v not in graph:
                graph[v] = {}
            if u not in graph[v]:
                graph[v][u] = 0
            graph[v][u] += path_flow
            v = parent[v]

    return max_flow

# Пример использования
if __name__ == "__main__":
    graph = read_graph_from_file('input.txt')

    source = input('Введите исток: ')
    sink = input('Введите сток: ')

    print("Максимальный поток %d" % ford_fulkerson(graph, source, sink))
