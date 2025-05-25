"""
Graph Algorithms Module
Handles path finding, connectivity analysis, and advanced graph algorithms
"""
from graph_generator import matrix_power

def find_paths_of_length(matrix: list[list[int]], length: int) -> list[tuple]:
    """Find all paths of given length using matrix powers"""
    matrix_power_result = matrix_power(matrix, length)
    paths = []
    
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix_power_result[i][j] > 0:
                # Find actual paths using DFS
                actual_paths = find_actual_paths(matrix, i, j, length)
                paths.extend(actual_paths)
    
    return paths

def find_actual_paths(matrix: list[list[int]], start: int, end: int, length: int) -> list[list[int]]:
    """Find actual paths between vertices using DFS"""
    def dfs(current: int, target: int, remaining: int, path: list[int]) -> list[list[int]]:
        if remaining == 0:
            return [path] if current == target else []
        
        paths = []
        for next_vertex in range(len(matrix)):
            if matrix[current][next_vertex] == 1:
                paths.extend(dfs(next_vertex, target, remaining - 1, path + [next_vertex]))
        
        return paths
    
    return dfs(start, end, length, [start])

def transitive_closure(matrix: list[list[int]]) -> list[list[int]]:
    """Calculate transitive closure using Floyd-Warshall algorithm"""
    n = len(matrix)
    # Initialize with original matrix
    closure = [row[:] for row in matrix]
    
    # Add self-loops for reachability
    for i in range(n):
        closure[i][i] = 1
    
    # Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                closure[i][j] = closure[i][j] or (closure[i][k] and closure[k][j])
    
    return closure

def strong_connectivity_matrix(matrix: list[list[int]]) -> list[list[int]]:
    """Calculate strong connectivity matrix"""
    reachability = transitive_closure(matrix)
    n = len(matrix)
    
    # Transpose matrix
    transpose = [[matrix[j][i] for j in range(n)] for i in range(n)]
    reachability_transpose = transitive_closure(transpose)
    
    # Strong connectivity: reachable in both directions
    strong_conn = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            strong_conn[i][j] = reachability[i][j] and reachability_transpose[i][j]
    
    return strong_conn

def find_strongly_connected_components(matrix: list[list[int]]) -> list[list[int]]:
    """Find strongly connected components"""
    strong_conn = strong_connectivity_matrix(matrix)
    n = len(matrix)
    visited = [False] * n
    components = []
    
    for i in range(n):
        if not visited[i]:
            component = []
            for j in range(n):
                if strong_conn[i][j] == 1:
                    component.append(j)
                    visited[j] = True
            components.append(component)
    
    return components

def create_condensation_graph(matrix: list[list[int]], components: list[list[int]]) -> list[list[int]]:
    """Create condensation graph from strongly connected components"""
    num_components = len(components)
    condensation = [[0 for _ in range(num_components)] for _ in range(num_components)]
    
    # Create mapping from vertex to component
    vertex_to_component = {}
    for comp_idx, component in enumerate(components):
        for vertex in component:
            vertex_to_component[vertex] = comp_idx
    
    # Build condensation graph
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 1:
                comp_i = vertex_to_component[i]
                comp_j = vertex_to_component[j]
                if comp_i != comp_j:
                    condensation[comp_i][comp_j] = 1
    
    return condensation