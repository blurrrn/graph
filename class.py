class Graph:
    def __init__(self, directed=False, weighted=False):
        # Инициализация графа
        self.adj_list = {}  # Список смежности
        self.directed = directed  # Флаг для ориентированного графа
        self.weighted = weighted  # Флаг для взвешенного графа

    @classmethod
    def from_file(cls, filename):
        # Метод класса для создания графа из файла
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

    def copy(self):
        # Метод для создания копии графа
        new_graph = Graph(self.directed, self.weighted)
        new_graph.adj_list = {u: v.copy() for u, v in self.adj_list.items()}
        return new_graph

    def add_versh(self, versh):
        # Метод для добавления вершины
        if versh not in self.adj_list:
            self.adj_list[versh] = {} if self.weighted else set()
        else:
            print(f"Вершина {versh} уже существует.")

    def add_edge(self, u, v, weight=None):
        # Метод для добавления ребра
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
        # Метод для удаления вершины
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

    def remove_edge(self, u, v):
        # Метод для удаления ребра
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

    def to_file(self, filename):
        # Метод для сохранения графа в файл
        with open(filename, 'w') as file:
            if self.directed:
                file.write("directed\n")
            if self.weighted:
                file.write("weighted\n")
            for u, edges in self.adj_list.items():
                for v, weight in (edges.items() if self.weighted else [(v, None) for v in edges]):
                    if weight is not None:
                        file.write(f"{u} {v} {weight}\n")
                    else:
                        file.write(f"{u} {v}\n")

    def display(self):
        # Метод для отображения графа
        for versh, edges in self.adj_list.items():
            if self.weighted:
                print(f"{versh}: {', '.join(f'{v}({w})' for v, w in edges.items())}")
            else:
                print(f"{versh}: {', '.join(edges)}")

# Минималистичный консольный интерфейс пользователя
def main():
    graph = Graph()

    while True:
        print("\n1. Добавить вершину")
        print("2. Добавить ребро")
        print("3. Удалить вершину")
        print("4. Удалить ребро")
        print("5. Показать графэ")
        print("6. Сохранить в файл")
        print("7. Загрузить из файла")
        print("8. Выйти")

        choice = input("Введите ваш выбор: ")

        if choice == '1':
            versh = input("Введите вершину: ")
            graph.add_versh(versh)
        elif choice == '2':
            u = input("Введите начальную вершину: ")
            v = input("Введите конечную вершину: ")
            weight = input("Введите вес (оставьте пустым, если граф невзвешенный): ")
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
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()
