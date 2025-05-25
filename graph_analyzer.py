"""
Graph Analyzer Module
Handles degree calculations, regularity checks, and basic graph properties
"""

def calculate_degrees(matrix: list[list[int]], is_directed: bool = False) -> dict:
    """Calculate vertex degrees"""
    n = len(matrix)
    result = {}
    
    if is_directed:
        # For directed graph: in-degree and out-degree
        in_degrees = [sum(matrix[j][i] for j in range(n)) for i in range(n)]
        out_degrees = [sum(matrix[i]) for i in range(n)]
        result = {
            'in_degrees': in_degrees,
            'out_degrees': out_degrees,
            'total_degrees': [in_degrees[i] + out_degrees[i] for i in range(n)]
        }
    else:
        # For undirected graph: simple degree (count each edge once, self-loops count as 2)
        degrees = []
        for i in range(n):
            degree = 0
            for j in range(n):
                if matrix[i][j] == 1:
                    if i == j:
                        degree += 2  # Self-loop counts as 2
                    else:
                        degree += 1
            degrees.append(degree)
        result = {'degrees': degrees}
    
    return result

def is_regular_graph(degrees: list[int]) -> tuple[bool, int]:
    """Check if graph is regular and return regularity degree"""
    if not degrees:
        return False, 0
    
    first_degree = degrees[0]
    is_regular = all(deg == first_degree for deg in degrees)
    return is_regular, first_degree if is_regular else 0

def find_special_vertices(degrees: list[int]) -> dict:
    """Find hanging (degree 1) and isolated (degree 0) vertices"""
    hanging = [i for i, deg in enumerate(degrees) if deg == 1]
    isolated = [i for i, deg in enumerate(degrees) if deg == 0]
    return {'hanging': hanging, 'isolated': isolated}

def format_paths_compact(paths: list[list[int]], paths_per_line: int = 4) -> str:
    """Format paths in compact horizontal layout"""
    if not paths:
        return "  Немає шляхів\n"
    
    result = ""
    for i in range(0, len(paths), paths_per_line):
        line_paths = paths[i:i + paths_per_line]
        path_strings = []
        for path in line_paths:
            path_str = "→".join(map(str, path))
            path_strings.append(path_str)
        result += "  " + " | ".join(path_strings) + "\n"
    
    result += f"\nЗагальна кількість шляхів: {len(paths)}\n"
    return result