def remove_edges_to_hanging_vertices(self):
        hanging_vertices = []
        for vertex in self.adj_list:
            out_degree = len(self.adj_list[vertex])
            in_degree = 0
            for u, edges in self.adj_list.items():
                if vertex in edges:
                    in_degree += 1

            if self.directed:
                if in_degree == 1 and out_degree == 0:
                    hanging_vertices.append(vertex)
            else:
                if out_degree == 1:
                    hanging_vertices.append(vertex)
for vertex in hanging_vertices:
            for u, edges in self.adj_list.items():
                if vertex in edges:
                    if self.weighted:
                        del self.adj_list[u][vertex]
                    else:
                        self.adj_list[u].remove(vertex)
