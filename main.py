"""
Main Application Module
Handles GUI, user interaction, and coordinates all other modules
"""
import tkinter as tk
from tkinter import ttk, scrolledtext

from graph_generator import generate_Adir, make_Aundir, matrix_power, calculate_grid_size
from graph_analyzer import calculate_degrees, is_regular_graph, find_special_vertices, format_paths_compact
from graph_algorithms import (find_paths_of_length, transitive_closure, strong_connectivity_matrix,
                             find_strongly_connected_components, create_condensation_graph)
from graph_visualizer import GraphVisualizer

class GraphAnalyzer:
    def __init__(self, root):
        self.root = root
        
        # Input parameters
        self.n1, self.n2, self.n3, self.n4 = 4, 1, 3, 2
        self.n = 10 + self.n3  # 13 vertices
        self.seed = int(f"{self.n1}{self.n2}{self.n3}{self.n4}")
        
        # Two different k coefficients for different parts
        self.k1 = 1.0 - self.n3 * 0.01 - self.n4 * 0.01 - 0.3  # For first part
        self.k2 = 1.0 - self.n3 * 0.005 - self.n4 * 0.005 - 0.27  # For second part
        
        # Dynamic grid size calculation
        self.rows, self.cols = calculate_grid_size(self.n)
        
        # Generate matrices
        self.Adir1 = generate_Adir(self.n, self.k1, self.seed)
        self.Aundir1 = make_Aundir(self.Adir1)
        self.Adir2 = generate_Adir(self.n, self.k2, self.seed)
        
        self.current_matrix = self.Adir1
        self.current_type = "directed1"
        
        self.setup_ui()
        self.setup_visualizer()
        self.analyze_graphs()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Canvas
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(left_frame, width=600, height=600, bg='white')
        self.canvas.pack()
        
        # Buttons for graph switching
        button_frame = tk.Frame(left_frame)
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="Directed (k1)", command=lambda: self.switch_graph("directed1")).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Undirected (k1)", command=lambda: self.switch_graph("undirected1")).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Directed (k2)", command=lambda: self.switch_graph("directed2")).pack(side=tk.LEFT, padx=2)
        tk.Button(button_frame, text="Condensation", command=lambda: self.switch_graph("condensation")).pack(side=tk.LEFT, padx=2)
        
        # Right side - Results
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Notebook for different result tabs
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_results_tabs()
    
    def setup_visualizer(self):
        """Initialize the graph visualizer"""
        self.visualizer = GraphVisualizer(self.canvas)
        self.visualizer.calculate_positions(self.n, self.rows, self.cols)
        
    def create_results_tabs(self):
        # Tab 1: Basic Analysis
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Basic Analysis")
        self.results_text1 = scrolledtext.ScrolledText(tab1, wrap=tk.WORD, width=60, height=30, font=("Consolas", 9))
        self.results_text1.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 2: Paths and Connectivity
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="Paths & Connectivity")
        self.results_text2 = scrolledtext.ScrolledText(tab2, wrap=tk.WORD, width=60, height=30, font=("Consolas", 9))
        self.results_text2.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 3: Matrices
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="Matrices")
        self.results_text3 = scrolledtext.ScrolledText(tab3, wrap=tk.WORD, width=60, height=30, font=("Consolas", 9))
        self.results_text3.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def switch_graph(self, graph_type):
        self.current_type = graph_type
        if graph_type == "directed1":
            self.current_matrix = self.Adir1
        elif graph_type == "undirected1":
            self.current_matrix = self.Aundir1
        elif graph_type == "directed2":
            self.current_matrix = self.Adir2
        elif graph_type == "condensation":
            components = find_strongly_connected_components(self.Adir2)
            self.current_matrix = create_condensation_graph(self.Adir2, components)
            
        self.draw_graph()
    
    def draw_graph(self):
        self.visualizer.clear_canvas()
        matrix = self.current_matrix
        
        # Adjust positions for condensation graph
        if self.current_type == "condensation":
            components = find_strongly_connected_components(self.Adir2)
            positions = self.visualizer.get_condensation_positions(len(components))
            node_labels = [f"C{i}" for i in range(len(components))]
            self.visualizer.positions = positions  # Update visualizer positions
        else:
            positions = self.visualizer.positions
            node_labels = [str(i) for i in range(self.n)]
        
        # SMART EDGE DRAWING WITH COLLISION AVOIDANCE
        if self.current_type == "undirected1":
            # For undirected graphs: process only upper triangle to avoid duplicates
            for i in range(len(matrix)):
                if i >= len(positions):
                    break
                for j in range(i, len(matrix)):  # Start from i, not 0
                    if j >= len(positions):
                        break
                    if matrix[i][j] == 1:
                        x1, y1 = positions[i]
                        x2, y2 = positions[j]
                        
                        if i == j:
                            # Self-loop
                            self.visualizer.draw_self_loop(x1, y1, with_arrow=False)
                        else:
                            # Smart routing for undirected edge
                            self.visualizer.draw_smart_line((x1, y1), (x2, y2), with_arrow=False)
        else:
            # For directed graphs: process all edges normally with smart routing
            for i in range(len(matrix)):
                if i >= len(positions):
                    break
                x1, y1 = positions[i]
                for j in range(len(matrix)):
                    if j >= len(positions):
                        break
                    if matrix[i][j] == 1:
                        x2, y2 = positions[j]
                        
                        if i == j:
                            # Self-loop with arrow
                            self.visualizer.draw_self_loop(x1, y1, with_arrow=True)
                        else:
                            # Smart routing for directed edge with arrow
                            self.visualizer.draw_smart_line((x1, y1), (x2, y2), with_arrow=True)
        
        # Draw nodes on top of edges
        for i, (x, y) in enumerate(positions):
            if i >= len(node_labels):
                break
            self.visualizer.draw_node(x, y, node_labels[i])
    
    def analyze_graphs(self):
        # Clear all result areas
        self.results_text1.delete(1.0, tk.END)
        self.results_text2.delete(1.0, tk.END)
        self.results_text3.delete(1.0, tk.END)
        
        # Part 1 Analysis
        self.results_text1.insert(tk.END, f"ЛАБОРАТОРНА РОБОТА 4 - АНАЛІЗ ГРАФІВ\n")
        self.results_text1.insert(tk.END, f"Параметри: n1={self.n1}, n2={self.n2}, n3={self.n3}, n4={self.n4}\n")
        self.results_text1.insert(tk.END, f"Вершини: {self.n}\n")
        self.results_text1.insert(tk.END, f"k1 = {self.k1:.3f}, k2 = {self.k2:.3f}\n\n")
        
        # Analyze first graph (k1)
        self.results_text1.insert(tk.END, "=== ЧАСТИНА 1: БАЗОВИЙ АНАЛІЗ (k1) ===\n\n")
        
        # Directed graph degrees
        dir_degrees = calculate_degrees(self.Adir1, is_directed=True)
        self.results_text1.insert(tk.END, "Аналіз напрямленого графа:\n")
        self.results_text1.insert(tk.END, f"Напівстепені заходу:  {dir_degrees['in_degrees']}\n")
        self.results_text1.insert(tk.END, f"Напівстепені виходу: {dir_degrees['out_degrees']}\n")
        self.results_text1.insert(tk.END, f"Повні степені:       {dir_degrees['total_degrees']}\n\n")
        
        # Undirected graph degrees
        undir_degrees = calculate_degrees(self.Aundir1, is_directed=False)
        self.results_text1.insert(tk.END, "Аналіз ненапрямленого графа:\n")
        self.results_text1.insert(tk.END, f"Степені вершин: {undir_degrees['degrees']}\n\n")
        
        # Check regularity
        is_reg_dir, reg_deg_dir = is_regular_graph(dir_degrees['total_degrees'])
        is_reg_undir, reg_deg_undir = is_regular_graph(undir_degrees['degrees'])
        
        self.results_text1.insert(tk.END, f"Напрямлений граф регулярний: {is_reg_dir}")
        if is_reg_dir:
            self.results_text1.insert(tk.END, f" (степінь {reg_deg_dir})")
        self.results_text1.insert(tk.END, f"\n")
        
        self.results_text1.insert(tk.END, f"Ненапрямлений граф регулярний: {is_reg_undir}")
        if is_reg_undir:
            self.results_text1.insert(tk.END, f" (степінь {reg_deg_undir})")
        self.results_text1.insert(tk.END, f"\n\n")
        
        # Special vertices
        special_dir = find_special_vertices(dir_degrees['total_degrees'])
        special_undir = find_special_vertices(undir_degrees['degrees'])
        
        self.results_text1.insert(tk.END, f"Напрямлений граф:\n")
        self.results_text1.insert(tk.END, f"  Висячі вершини:    {special_dir['hanging'] if special_dir['hanging'] else 'Немає'}\n")
        self.results_text1.insert(tk.END, f"  Ізольовані вершини: {special_dir['isolated'] if special_dir['isolated'] else 'Немає'}\n\n")
        
        self.results_text1.insert(tk.END, f"Ненапрямлений граф:\n")
        self.results_text1.insert(tk.END, f"  Висячі вершини:    {special_undir['hanging'] if special_undir['hanging'] else 'Немає'}\n")
        self.results_text1.insert(tk.END, f"  Ізольовані вершини: {special_undir['isolated'] if special_undir['isolated'] else 'Немає'}\n\n")
        
        # Part 2 Analysis
        self.results_text2.insert(tk.END, "=== ЧАСТИНА 2: РОЗШИРЕНИЙ АНАЛІЗ (k2) ===\n\n")
        
        # Semi-degrees for new graph
        dir_degrees2 = calculate_degrees(self.Adir2, is_directed=True)
        self.results_text2.insert(tk.END, "Новий напрямлений граф (k2) - напівстепені:\n")
        self.results_text2.insert(tk.END, f"Напівстепені заходу:  {dir_degrees2['in_degrees']}\n")
        self.results_text2.insert(tk.END, f"Напівстепені виходу: {dir_degrees2['out_degrees']}\n\n")
        
        # Paths of length 2 and 3 with compact formatting
        self.results_text2.insert(tk.END, "Шляхи довжини 2:\n")
        paths_2 = find_paths_of_length(self.Adir2, 2)
        compact_paths_2 = format_paths_compact(paths_2, 5)  # type: ignore # 5 paths per line
        self.results_text2.insert(tk.END, compact_paths_2)
        self.results_text2.insert(tk.END, "\n")
        
        self.results_text2.insert(tk.END, "Шляхи довжини 3:\n")
        paths_3 = find_paths_of_length(self.Adir2, 3)
        compact_paths_3 = format_paths_compact(paths_3, 4)  # type: ignore # 4 paths per line (longer paths)
        self.results_text2.insert(tk.END, compact_paths_3)
        self.results_text2.insert(tk.END, "\n")
        
        # Strongly connected components
        components = find_strongly_connected_components(self.Adir2)
        self.results_text2.insert(tk.END, "Компоненти сильної зв'язності:\n")
        for i, comp in enumerate(components):
            self.results_text2.insert(tk.END, f"  Компонента {i}: {comp}\n")
        self.results_text2.insert(tk.END, f"\nЗагальна кількість компонент: {len(components)}\n\n")
        
        # Matrices
        self.results_text3.insert(tk.END, "=== МАТРИЦІ ===\n\n")
        
        # Original matrices
        self.results_text3.insert(tk.END, "Матриця суміжності напрямленого графа (k1):\n")
        for row in self.Adir1:
            self.results_text3.insert(tk.END, f"{row}\n")
        self.results_text3.insert(tk.END, "\n")
        
        self.results_text3.insert(tk.END, "Матриця суміжності ненапрямленого графа (k1):\n")
        for row in self.Aundir1:
            self.results_text3.insert(tk.END, f"{row}\n")
        self.results_text3.insert(tk.END, "\n")
        
        self.results_text3.insert(tk.END, "Матриця суміжності напрямленого графа (k2):\n")
        for row in self.Adir2:
            self.results_text3.insert(tk.END, f"{row}\n")
        self.results_text3.insert(tk.END, "\n")
        
        # A^2 and A^3 matrices
        A2 = matrix_power(self.Adir2, 2)
        A3 = matrix_power(self.Adir2, 3)
        
        self.results_text3.insert(tk.END, "Матриця A² (шляхи довжини 2):\n")
        for row in A2:
            self.results_text3.insert(tk.END, f"{row}\n")
        self.results_text3.insert(tk.END, "\n")
        
        self.results_text3.insert(tk.END, "Матриця A³ (шляхи довжини 3):\n")
        for row in A3:
            self.results_text3.insert(tk.END, f"{row}\n")
        self.results_text3.insert(tk.END, "\n")
        
        # Reachability matrix
        reachability = transitive_closure(self.Adir2)
        self.results_text3.insert(tk.END, "Матриця досяжності:\n")
        for row in reachability:
            self.results_text3.insert(tk.END, f"{row}\n")
        self.results_text3.insert(tk.END, "\n")
        
        # Strong connectivity matrix
        strong_conn = strong_connectivity_matrix(self.Adir2)
        self.results_text3.insert(tk.END, "Матриця сильної зв'язності:\n")
        for row in strong_conn:
            self.results_text3.insert(tk.END, f"{row}\n")
        self.results_text3.insert(tk.END, "\n")
        
        # Condensation matrix
        condensation = create_condensation_graph(self.Adir2, components)
        self.results_text3.insert(tk.END, "Матриця графа конденсації:\n")
        for row in condensation:
            self.results_text3.insert(tk.END, f"{row}\n")
        
        # Draw initial graph
        self.draw_graph()

def main():
    root = tk.Tk()
    root.title("Лабораторна робота 4 - Аналіз графів")
    root.geometry("1400x800")
    
    app = GraphAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()