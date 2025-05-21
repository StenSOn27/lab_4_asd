import tkinter as tk
import random
import math
import numpy as np
from collections import deque, defaultdict

# Input parameters
n1, n2, n3, n4 = 4, 1, 3, 2
n = 10 + n3  # 13 vertices
seed = int(f"{n1}{n2}{n3}{n4}")
random.seed(seed)

# Initial coefficient for task 1
k = 1.0 - n3 * 0.01 - n4 * 0.01 - 0.3

ROWS, COLS = math.ceil(n / 4), 4  # Rectangular layout

def generate_Adir(n, k):
    return [[0 if random.uniform(0, 2.0) * k < 1.0 else 1 for _ in range(n)] for _ in range(n)]

def make_Aundir(Adir):
    return [[1 if Adir[i][j] or Adir[j][i] else 0 for j in range(n)] for i in range(n)]

def print_matrix(name, M):
    print(f"{name}:")
    for row in M:
        print(row)
    print()

def degree_info(matrix, directed=True):
    if directed:
        in_deg = [sum(row[i] for row in matrix) for i in range(n)]
        out_deg = [sum(row) for row in matrix]
        return in_deg, out_deg
    else:
        return [sum(row) for row in matrix],

def is_regular(degrees):
    return all(d == degrees[0] for d in degrees)

def hanging_isolated(degrees):
    hanging = [i for i, d in enumerate(degrees) if d == 1]
    isolated = [i for i, d in enumerate(degrees) if d == 0]
    return hanging, isolated

def power_matrix(A, power):
    result = np.linalg.matrix_power(np.array(A), power)
    return result.tolist()

def reachability_matrix(A):
    n = len(A)
    R = [[int(i == j or A[i][j]) for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                R[i][j] = R[i][j] or (R[i][k] and R[k][j])
    return R

def strongly_connected_components(R):
    n = len(R)
    visited = [False] * n
    components = []
    for i in range(n):
        if not visited[i]:
            comp = [j for j in range(n) if R[i][j] and R[j][i]]
            for j in comp:
                visited[j] = True
            components.append(comp)
    return components

def condense_graph(components, A):
    mapping = {}
    for idx, comp in enumerate(components):
        for v in comp:
            mapping[v] = idx
    size = len(components)
    cond = [[0]*size for _ in range(size)]
    for i in range(n):
        for j in range(n):
            if A[i][j] and mapping[i] != mapping[j]:
                cond[mapping[i]][mapping[j]] = 1
    return cond

class GraphVisualizer:
    def __init__(self, root, matrix, title, directed=True):
        self.root = root
        self.canvas_size = 700
        self.margin = 60
        self.node_radius = 15
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg='white')
        self.canvas.pack()
        self.positions = self.calculate_positions()
        self.draw_graph(matrix, directed, title)

    def calculate_positions(self):
        positions = []
        for r in range(ROWS):
            for c in range(COLS):
                if len(positions) < n:
                    x = self.margin + c * ((self.canvas_size - 2 * self.margin) / (COLS - 1))
                    y = self.margin + r * ((self.canvas_size - 2 * self.margin) / (ROWS - 1))
                    positions.append((x, y))
        return positions

    def draw_graph(self, matrix, directed, title):
        self.canvas.create_text(self.canvas_size / 2, 20, text=title, font=("Arial", 16, "bold"))
        for i in range(n):
            x1, y1 = self.positions[i]
            for j in range(n):
                if matrix[i][j]:
                    x2, y2 = self.positions[j]
                    if i != j:
                        dx, dy = x2 - x1, y2 - y1
                        dist = math.hypot(dx, dy)
                        offset_x = dx / dist * self.node_radius
                        offset_y = dy / dist * self.node_radius
                        start = x1 + offset_x, y1 + offset_y
                        end = x2 - offset_x, y2 - offset_y
                        self.canvas.create_line(start, end, arrow=tk.LAST if directed else None)
        for i, (x, y) in enumerate(self.positions):
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius, x + self.node_radius, y + self.node_radius, fill="lightblue")
            self.canvas.create_text(x, y, text=str(i))

def main():
    Adir = generate_Adir(n, k)
    Aundir = make_Aundir(Adir)

    print_matrix("Adir", Adir)
    print_matrix("Aundir", Aundir)

    in_deg, out_deg = degree_info(Adir)
    undeg, = degree_info(Aundir, directed=False)

    print("In-degrees:", in_deg)
    print("Out-degrees:", out_deg)
    print("Undirected degrees:", undeg)

    print("Directed Regular:", is_regular(out_deg + in_deg))
    print("Undirected Regular:", is_regular(undeg))

    h, iso = hanging_isolated(undeg)
    print("Hanging vertices:", h)
    print("Isolated vertices:", iso)

    # Second task: new k
    k2 = 1.0 - n3 * 0.005 - n4 * 0.005 - 0.27
    Adir2 = generate_Adir(n, k2)

    print_matrix("Adir (new k)", Adir2)
    in2, out2 = degree_info(Adir2)
    print("New In-degrees:", in2)
    print("New Out-degrees:", out2)

    A2 = power_matrix(Adir2, 2)
    A3 = power_matrix(Adir2, 3)

    print_matrix("A^2", A2)
    print_matrix("A^3", A3)

    R = reachability_matrix(Adir2)
    print_matrix("Reachability Matrix", R)

    components = strongly_connected_components(R)
    print("Strongly Connected Components:", components)

    cond_graph = condense_graph(components, Adir2)
    print_matrix("Condensation Graph", cond_graph)

    # Visualizations
    root1 = tk.Tk()
    GraphVisualizer(root1, Adir, "Directed Graph")
    root1.mainloop()

    root2 = tk.Tk()
    GraphVisualizer(root2, Aundir, "Undirected Graph", directed=False)
    root2.mainloop()

    root3 = tk.Tk()
    GraphVisualizer(root3, Adir2, "Modified Directed Graph")
    root3.mainloop()

    root4 = tk.Tk()
    GraphVisualizer(root4, cond_graph, "Condensation Graph")
    root4.mainloop()

if __name__ == "__main__":
    main()
