def remove_edges_to_hanging_vertices(self):
    # Найти все висячие вершины
    hanging_vertices = []
    for vertex in self.adj_list:
        if len(self.adj_list[vertex]) == 0:  # Вершина не имеет исходящих ребер
            incoming_edges = 0
            for u, edges in self.adj_list.items():
                if vertex in edges:
                    incoming_edges += 1
            if incoming_edges == 1:  # Вершина имеет только одно входящее ребро
                hanging_vertices.append(vertex)

    # Удалить ребра, ведущие в висячие вершины
    for vertex in hanging_vertices:
        for u, edges in self.adj_list.items():
            if vertex in edges:
                if self.weighted:
                    del self.adj_list[u][vertex]
                else:
                    self.adj_list[u].remove(vertex)

    print(f"Ребра, ведущие в висячие вершины, удалены.")

def remove_edges_to_hanging_vertices(self):
    # Найти все висячие вершины
    hanging_vertices = []
    for vertex in self.adj_list:
        if len(self.adj_list[vertex]) == 0:  # Вершина не имеет исходящих ребер
            incoming_edges = 0
            for u, edges in self.adj_list.items():
                if vertex in edges:
                    incoming_edges += 1
            if incoming_edges == 1:  # Вершина имеет только одно входящее ребро
                hanging_vertices.append(vertex)

    # Удалить ребра, ведущие в висячие вершины
    for vertex in hanging_vertices:
        for u, edges in self.adj_list.items():
            if vertex in edges:
                if self.weighted:
                    del self.adj_list[u][vertex]
                else:
                    self.adj_list[u].remove(vertex)

    # Удалить висячие вершины из списка смежности
    for vertex in hanging_vertices:
        if vertex in self.adj_list:
            del self.adj_list[vertex]

    print(f"Ребра, ведущие в висячие вершины, удалены.")
