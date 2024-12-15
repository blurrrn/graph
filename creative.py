import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import copy

class Graph:
    def __init__(self, directed=False, weighted=False, filename=None):
        self.adj_list = {}  # список смежности, ключ: вершина, значение: список соседей
        self.directed = directed
        self.weighted = weighted

        if filename:
            self.load_from_file(filename)

    def add_vertex(self, vertex):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, vertex1, vertex2, weight=None):
        if vertex1 in self.adj_list and vertex2 in self.adj_list:
            if self.weighted:
                if any(neighbor == (vertex2, weight) for neighbor in self.adj_list[vertex1]):
                    print(f"Ребро {vertex1} -> {vertex2} с весом {weight} уже существует.")
                    return
                elif any(neighbor[0] == vertex2 for neighbor in self.adj_list[vertex1]):
                    print(f"Ошибка: Ребро {vertex1} -> {vertex2} уже существует с другим весом.")
                    return
            else:
                if vertex2 in self.adj_list[vertex1] or (not self.directed and vertex1 in self.adj_list[vertex2]):
                    print(f"Ребро {vertex1} -> {vertex2} уже существует.")
                    return

            if self.weighted:
                self.adj_list[vertex1].append((vertex2, weight))
            else:
                self.adj_list[vertex1].append(vertex2)

            if not self.directed:
                if self.weighted:
                    if vertex1 != vertex2:
                        self.adj_list[vertex2].append((vertex1, weight))
                else:
                    if vertex1 != vertex2:
                        self.adj_list[vertex2].append(vertex1)

    def remove_vertex(self, vertex):
        if vertex in self.adj_list:
            del self.adj_list[vertex]

        for neighbors in self.adj_list.values():
            for n in neighbors[:]:
                if n == vertex or (isinstance(n, tuple) and n[0] == vertex):
                    neighbors.remove(n)

    def remove_edge(self, vertex1, vertex2):
        edge_found = False
        if vertex1 in self.adj_list:
            for neighbor in self.adj_list[vertex1][:]:
                if (isinstance(neighbor, tuple) and neighbor[0] == vertex2) or neighbor == vertex2:
                    self.adj_list[vertex1].remove(neighbor)
                    edge_found = True
                    break

        if not self.directed and vertex2 in self.adj_list:
            for neighbor in self.adj_list[vertex2][:]:
                if (isinstance(neighbor, tuple) and neighbor[0] == vertex1) or neighbor == vertex1:
                    self.adj_list[vertex2].remove(neighbor)
                    edge_found = True
                    break

        if edge_found:
            print(f"Ребро между {vertex1} и {vertex2} удалено.")
        else:
            print(f"Ошибка: Ребро между {vertex1} и {vertex2} не существует.")

    def display_info(self):
        info = f"Тип графа: {'Ориентированный' if self.directed else 'Неориентированный'}\n"
        info += f"Взвешенный: {'Да' if self.weighted else 'Нет'}\nСписок смежности:\n"
        for vertex, neighbors in self.adj_list.items():
            if self.weighted:
                neighbors_str = ", ".join(f"{n[0]} (вес: {n[1]})" for n in neighbors)
            else:
                neighbors_str = ", ".join(str(n) for n in neighbors)
            info += f"{vertex}: {neighbors_str if neighbors_str else ''}\n"
        messagebox.showinfo("Информация о графе", info)

    def save_to_file(self, filename):
        if not filename.endswith('.txt'):
            filename += '.txt'
        with open(filename, 'w') as f:
            f.write(f"{'Directed' if self.directed else 'Undirected'}\n")
            f.write(f"{'Yes' if self.weighted else 'No'}\n")
            written_edges = set()
            for vertex, neighbors in self.adj_list.items():
                if not neighbors:
                    f.write(f"{vertex}\n")
                for neighbor in neighbors:
                    if self.weighted:
                        edge = (vertex, neighbor[0]) if vertex <= neighbor[0] else (neighbor[0], vertex)
                        if edge not in written_edges:
                            f.write(f"{vertex} {neighbor[0]} {neighbor[1]}\n")
                            written_edges.add(edge)
                    else:
                        edge = (vertex, neighbor) if vertex <= neighbor else (neighbor, vertex)
                        if edge not in written_edges:
                            f.write(f"{vertex} {neighbor}\n")
                            written_edges.add(edge)

    def load_from_file(self, filename):
        if not filename.endswith('.txt'):
            filename += '.txt'
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.directed = "Directed" in lines[0]
            self.weighted = "Yes" in lines[1]
            for line in lines[2:]:
                data = line.strip().split()
                if len(data) == 1:
                    vertex = data[0]
                    self.add_vertex(vertex)
                elif len(data) == 2 or len(data) == 3:
                    vertex1 = data[0]
                    vertex2 = data[1]
                    self.add_vertex(vertex1)
                    self.add_vertex(vertex2)
                    if self.weighted and len(data) == 3:
                        weight = int(data[2])
                        self.add_edge(vertex1, vertex2, weight)
                    else:
                        self.add_edge(vertex1, vertex2)

    def copy(self):
        new_graph = Graph(directed=self.directed, weighted=self.weighted)
        new_graph.adj_list = copy.deepcopy(self.adj_list)
        return new_graph

    def kruskal_mst(self):
        if not self.weighted:
            messagebox.showinfo("Ошибка", "Граф должен быть взвешенным для выполнения алгоритма Краскала.")
            return
        if self.directed:
            messagebox.showinfo("Ошибка", "Алгоритм Краскала работает только с неориентированными графами.")
            return

        # Преобразуем рёбра в список и сортируем их по весу
        edges = []
        for vertex, neighbors in self.adj_list.items():
            for neighbor in neighbors:
                if isinstance(neighbor, tuple):  # Учитываем веса
                    edge = (vertex, neighbor[0], neighbor[1])
                    if edge not in edges and (neighbor[0], vertex, neighbor[1]) not in edges:
                        edges.append(edge)
        edges.sort(key=lambda x: x[2])  # Сортировка по весу

        # Union-Find структуры
        parent = {vertex: vertex for vertex in self.adj_list}
        rank = {vertex: 0 for vertex in self.adj_list}

        def find(vertex):
            if parent[vertex] != vertex:
                parent[vertex] = find(parent[vertex])  # Путь сжатия
            return parent[vertex]

        def union(v1, v2):
            root1 = find(v1)
            root2 = find(v2)
            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                elif rank[root1] < rank[root2]:
                    parent[root1] = root2
                else:
                    parent[root2] = root1
                    rank[root1] += 1

        # Построение MST
        mst = []
        for v1, v2, weight in edges:
            if find(v1) != find(v2):
                union(v1, v2)
                mst.append((v1, v2, weight))
                if len(mst) == len(self.adj_list) - 1:
                    break

        # Вывод результата
        if len(mst) == len(self.adj_list) - 1:
            result = "Минимальный каркас графа:\n" + "\n".join(f"{v1} - {v2}, вес: {weight}" for v1, v2, weight in mst)
            messagebox.showinfo("Минимальный каркас графа", result)
        else:
            messagebox.showinfo("Ошибка", "Граф несвязный, минимальный остов не может быть найден.")

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление графами")
        self.graphs = {}
        self.current_graph = None
        self.create_widgets()

    def create_widgets(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Button(button_frame, text="Выбрать граф", command=self.choose_graph).pack(fill=tk.X)
        tk.Button(button_frame, text="Добавить граф", command=self.add_graph).pack(fill=tk.X)
        tk.Button(button_frame, text="Добавить вершину", command=self.add_vertex).pack(fill=tk.X)
        tk.Button(button_frame, text="Добавить ребро", command=self.add_edge).pack(fill=tk.X)
        tk.Button(button_frame, text="Удалить вершину", command=self.remove_vertex).pack(fill=tk.X)
        tk.Button(button_frame, text="Удалить ребро", command=self.remove_edge).pack(fill=tk.X)
        tk.Button(button_frame, text="Показать информацию о графе", command=self.display_info).pack(fill=tk.X)
        tk.Button(button_frame, text="Сохранить граф", command=self.save_graph).pack(fill=tk.X)
        tk.Button(button_frame, text="Загрузить граф", command=self.load_graph).pack(fill=tk.X)
        tk.Button(button_frame, text="Создать копию графа", command=self.copy_graph).pack(fill=tk.X)
        tk.Button(button_frame, text="Найти минимальный остов (Краскал)", command=self.find_mst).pack(fill=tk.X)
        tk.Button(button_frame, text="Показать граф", command=self.display_graph).pack(fill=tk.X)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def choose_graph(self):
        if not self.graphs:
            messagebox.showinfo("Ошибка", "Нет доступных графов.")
            return
        graph_name = simpledialog.askstring("Выбрать граф", "Введите имя графа:")
        if graph_name in self.graphs:
            self.current_graph = self.graphs[graph_name]
            messagebox.showinfo("Успешно", f"Граф '{graph_name}' выбран.")
        else:
            messagebox.showinfo("Ошибка", f"Граф с именем '{graph_name}' не найден.")

    def add_graph(self):
        graph_name = simpledialog.askstring("Ввод", "Введите имя для нового графа:")
        directed = messagebox.askyesno("Ориентированный?", "Граф ориентированный?")
        weighted = messagebox.askyesno("Взвешенный?", "Граф взвешенный?")
        if graph_name and graph_name not in self.graphs:
            self.graphs[graph_name] = Graph(directed=directed, weighted=weighted)
            self.current_graph = self.graphs[graph_name]
            messagebox.showinfo("Успешно", f"Граф '{graph_name}' создан.")
        else:
            messagebox.showwarning("Ошибка", "Неверное имя или граф уже существует.")

    def add_vertex(self):
        if not self.current_graph:
            messagebox.showwarning("Ошибка", "Нет выбранного графа.")
            return
        vertex = simpledialog.askstring("Ввод", "Введите имя вершины:")
        if vertex:
            self.current_graph.add_vertex(vertex)
            messagebox.showinfo("Успешно", f"Вершина '{vertex}' добавлена.")

    def add_edge(self):
        if not self.current_graph:
            messagebox.showwarning("Ошибка", "Нет выбранного графа.")
            return
        vertex1 = simpledialog.askstring("Ввод", "Введите первую вершину:")
        vertex2 = simpledialog.askstring("Ввод", "Введите вторую вершину:")
        if self.current_graph.weighted:
            weight = simpledialog.askinteger("Ввод", "Введите вес ребра:")
            self.current_graph.add_edge(vertex1, vertex2, weight)
        else:
            self.current_graph.add_edge(vertex1, vertex2)
        messagebox.showinfo("Успешно", f"Ребро '{vertex1} -> {vertex2}' добавлено.")

    def remove_vertex(self):
        if not self.current_graph:
            messagebox.showwarning("Ошибка", "Нет выбранного графа.")
            return
        vertex = simpledialog.askstring("Ввод", "Введите вершину для удаления:")
        self.current_graph.remove_vertex(vertex)
        messagebox.showinfo("Успешно", f"Вершина '{vertex}' удалена.")

    def remove_edge(self):
        if not self.current_graph:
            messagebox.showwarning("Ошибка", "Нет выбранного графа.")
            return
        vertex1 = simpledialog.askstring("Ввод", "Введите первую вершину:")
        vertex2 = simpledialog.askstring("Ввод", "Введите вторую вершину:")
        self.current_graph.remove_edge(vertex1, vertex2)

    def display_info(self):
        if not self.current_graph:
            messagebox.showwarning("Ошибка", "Нет выбранного графа.")
            return
        self.current_graph.display_info()

    def save_graph(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            self.current_graph.save_to_file(filename)
            messagebox.showinfo("Успешно", f"Граф сохранен в '{filename}'.")

    def load_graph(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            graph_name = simpledialog.askstring("Ввод", "Введите имя загружаемого графа:")
            if graph_name and graph_name not in self.graphs:
                self.graphs[graph_name] = Graph(filename=filename)
                self.current_graph = self.graphs[graph_name]
                messagebox.showinfo("Успешно", f"Граф '{graph_name}' загружен.")
            else:
                messagebox.showwarning("Ошибка", "Неверное имя или граф уже существует.")

    def copy_graph(self):
        if not self.current_graph:
            messagebox.showwarning("Ошибка", "Нет выбранного графа.")
            return
        graph_copy_name = simpledialog.askstring("Ввод", "Введите имя для копии графа:")
        if graph_copy_name:
            self.graphs[graph_copy_name] = self.current_graph.copy()
            messagebox.showinfo("Успешно", f"Копия графа сохранена под именем '{graph_copy_name}'.")

    def find_mst(self):
        if not self.current_graph:
            messagebox.showwarning("Ошибка", "Нет выбранного графа.")
            return
        self.current_graph.kruskal_mst()

    def display_graph(self):
        if not self.current_graph:
            messagebox.showwarning("Ошибка", "Нет выбранного графа.")
            return
        G = nx.DiGraph() if self.current_graph.directed else nx.Graph()
        for vertex, neighbors in self.current_graph.adj_list.items():
            for neighbor in neighbors:
                if isinstance(neighbor, tuple):
                    G.add_edge(vertex, neighbor[0], weight=neighbor[1])
                else:
                    G.add_edge(vertex, neighbor)
        plt.figure(figsize=(6, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray")
        if self.current_graph.weighted:
            labels = nx.get_edge_attributes(G, "weight")
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        fig = plt.gcf()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)

root = tk.Tk()
app = GraphApp(root)
root.mainloop()
