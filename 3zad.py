class Graph:
    # инициализация графа
    def __init__(self, directed=False, weighted=False):
        self.adj_list = {}  # Список смежности
        self.directed = directed  # флаг для ориентированного графа
        self.weighted = weighted  # флаг для взвешенного графа

        # создание графа из файла
    @classmethod
    def from_file(cls, filename):
        graph = cls()
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('directed'):
                    graph.directed = True
                elif line.startswith('weighted'):
                    graph.weighted = True
                else:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        u, v = parts
                        graph.add_edge(u, v)
                    elif len(parts) == 3:
                        u, v, w = parts
                        graph.add_edge(u, v, int(w))
        return graph

        # метод для создания копии графа
    def copy(self):
        new_graph = Graph(self.directed, self.weighted)
        # копирование списка смежности
        new_graph.adj_list = {u: v.copy() for u, v in self.adj_list.items()}
        return new_graph

        # добавление вершины
    def add_versh(self, versh):
        if versh not in self.adj_list:
            self.adj_list[versh] = {} if self.weighted else set()
        else:
            print(f"Вершина {versh} уже существует.")

    # добавление ребра
    def add_edge(self, u, v, weight=None):
        if u not in self.adj_list:
            self.add_versh(u)
        if v not in self.adj_list:
            self.add_versh(v)

        if self.weighted:
            self.adj_list[u][v] = weight
            if not self.directed:
                self.adj_list[v][u] = weight
        else:
            self.adj_list[u].add(v)
            if not self.directed:
                self.adj_list[v].add(u)

    def remove_versh(self, versh):
        # удаление вершины
        if versh in self.adj_list:
            del self.adj_list[versh]
            for v in self.adj_list:
                if self.weighted:
                    if versh in self.adj_list[v]:
                        del self.adj_list[v][versh]
                else:
                    self.adj_list[v].discard(versh)
        else:
            print(f"Вершина {versh} не существует.")

        # удаление ребра
    def remove_edge(self, u, v):
        if u in self.adj_list and v in self.adj_list[u]:
            if self.weighted:
                del self.adj_list[u][v]
                if not self.directed:
                    del self.adj_list[v][u]
            else:
                self.adj_list[u].remove(v)
                if not self.directed:
                    self.adj_list[v].remove(u)
        else:
            print(f"Ребро ({u}, {v}) не существует.")

        # сохранение графа в файл

    def to_file(self, filename):
        with open(filename, 'w') as file:
            if self.directed:
                file.write("directed\n")
            if self.weighted:
                file.write("weighted\n")

            for u, edges in self.adj_list.items():

                if not edges:
                    file.write(f"{u}\n")
                else:
                    for v, weight in (edges.items() if self.weighted else [(v, None) for v in edges]):
                        if weight is not None:
                            file.write(f"{u} {v} {weight}\n")
                        else:
                            file.write(f"{u} {v}\n")

        # отображение графа пользовател.
    def display(self):
        for versh, edges in self.adj_list.items():
            if self.weighted:
                print(f"{versh}: {', '.join(f'{v}({w})' for v, w in edges.items())}")
            else:
                print(f"{versh}: {', '.join(edges)}")

    def LA2(self, versh):
        if self.directed:
            if versh not in self.adj_list:
                print(f"Вершина '{versh}' не найдена в графе.")
                return
            in_degrees = {v: 0 for v in self.adj_list}
            for u ,edges in self.adj_list.items():
                for v in edges:
                    in_degrees[v] += 1
            target_in_degree = in_degrees[versh]
            if target_in_degree == 0:
                print("Полустепень захода заданной вершины равно нулю.")
            else:
                result = [v for v, degree in in_degrees.items() if degree < target_in_degree]
                print(f"Вершины с меньшей полустепенью захода, чем у вершины {versh}: {', '.join(result)}")
        else:
            print(f"Граф не ориентированный.")

    def remove_edges_to_hanging_vertices(self):
        hanging_vertices = []
        for versh in self.adj_list:
            out_degree = len(self.adj_list[versh])
            in_degree = 0
            for u, edges in self.adj_list.items():
                if versh in edges:
                    in_degree += 1

            if self.directed:
                if in_degree == 1 and out_degree == 0:
                    hanging_vertices.append(versh)
            else:
                if out_degree == 1:
                    hanging_vertices.append(versh)

        for versh in hanging_vertices:
            for u, edges in self.adj_list.items():
                if versh in edges:
                    if self.weighted:
                        del self.adj_list[u][versh]
                    else:
                        self.adj_list[u].remove(versh)
                    if not self.directed:
                        if self.weighted:
                            del self.adj_list[versh][u]
                        else:
                            self.adj_list[versh].remove(u)

        print(f"Ребра, ведущие в висячие вершины, удалены.")

# консольный интерфейс
def main():
    graph = Graph()

    while True:
        print("\n1 - Добавить вершину")
        print("2 - Добавить ребро")
        print("3 - Удалить вершину")
        print("4 - Удалить ребро")
        print("5 - Показать граф")
        print("6 - Сохранить в файл")
        print("7 - Загрузить из файла")
        print("8 - Задание на полустепень захода")
        print("9 - Висячие вершины")
        print("10 - Выйти")

        choice = input("Введите ваш выбор: ")

        if choice == '1':
            versh = input("Введите вершину: ")
            graph.add_versh(versh)
        elif choice == '2':
            u = input("Введите начальную вершину: ")
            v = input("Введите конечную вершину: ")
            weight = input("Введите вес (ничего, если граф невзвешенный): ")
            graph.add_edge(u, v, int(weight) if weight else None)
        elif choice == '3':
            versh = input("Введите вершину для удаления: ")
            graph.remove_versh(versh)
        elif choice == '4':
            u = input("Введите начальную вершину: ")
            v = input("Введите конечную вершину: ")
            graph.remove_edge(u, v)
        elif choice == '5':
            graph.display()
        elif choice == '6':
            filename = input("Введите имя файла для сохранения: ")
            graph.to_file(filename)
        elif choice == '7':
            filename = input("Введите имя файла для загрузки: ")
            graph = Graph.from_file(filename)
        elif choice == '8':
            versh = input('Введите вершину: ')
            graph.LA2(versh)
        elif choice == '9':
            graph.remove_edges_to_hanging_vertices()
        elif choice == '10':
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()
