class Graph:
    def __init__(self, weighted=True):
        self.weighted = weighted
        self.adjacency_list = {}
        self.weights = {}

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                u, v, weight = line.strip().split()
                weight = int(weight)
                if u not in self.adjacency_list:
                    self.adjacency_list[u] = []
                if v not in self.adjacency_list:
                    self.adjacency_list[v] = []
                self.adjacency_list[u].append(v)
                self.adjacency_list[v].append(u)
                self.weights[(u, v)] = weight
                self.weights[(v, u)] = weight

    def find_minimal_spanning_tree_kruskal(self):
        if not self.weighted:
            print("Граф не взвешенный. Алгоритм Краскала применим только к взвешенным графам.")
            return None

        mst_edges = []  # список ребер составляющий мин остов дерево
        total_weight = 0  # общий вес дерева

        edges = sorted(self.weights.items(), key=lambda x: x[1])  # сортируем ребра по возрастанию веса

        parent = {node: node for node in self.adjacency_list}  # словарь родителей (изначально каждый узел сам себе предок)
        rank = {node: 0 for node in self.adjacency_list}  # уровень узла (изначально каждый узел корень своего дерева (уровень 0))

        def find(node):  # метод для поиска корневого предка узла
            if parent[node] != node:
                parent[node] = find(parent[node])  # рекурсивно вызываем
            return parent[node]

        def union(node1, node2):  # метод для объединения двух поддеревьев
            root1 = find(node1)  # ищем предка первого узла
            root2 = find(node2)  # ищем предка второго узла
            if root1 != root2:  # если предки не совпали сравниванием уровень чтобы сохранить баланс
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                elif rank[root1] < rank[root2]:
                    parent[root1] = root2
                else:
                    parent[root2] = root1
                    rank[root1] += 1

        for (u, v), weight in edges:  # идем по всем ребрам в порядке возрастания весов
            if find(u) != find(v):  # если у узлов не один и тот же предок, то есть нет цикла
                union(u, v)  # объединяем их в поддерево
                mst_edges.append((u, v, weight))  # добавляем в результат
                total_weight += weight  # добавляем весь вес дерева

                if len(mst_edges) == len(self.adjacency_list) - 1:  # если добавлены все узлы (значит ребер n - 1)
                    # можно закончить цикл
                    break

        print("Минимальный остовный каркас:")
        for u, v, weight in mst_edges:
            print(f"{u} - {v} : {weight}")
        print(f"Общий вес каркаса: {total_weight}")

        return mst_edges, total_weight

graph = Graph()
graph.load_from_file('input.txt')
mst_edges, total_weight = graph.find_minimal_spanning_tree_kruskal()
