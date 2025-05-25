"""
Graph Generator Module
Handles matrix generation and basic graph operations
"""
import random
import math

def generate_Adir(n: int, k: float, seed: int) -> list[list[int]]:
    """Generate directed adjacency matrix with given coefficient k"""
    random.seed(seed)  # Reset seed for consistency
    return [
        [0 if random.uniform(0, 2.0) * k < 1.0 else 1 for _ in range(n)]
        for _ in range(n)
    ]

def make_Aundir(Adir: list[list[int]]) -> list[list[int]]:
    """Convert directed matrix to undirected - FIXED VERSION"""
    n = len(Adir)
    Aundir = [[0 for _ in range(n)] for _ in range(n)]
    
    # Process each pair of vertices only once to ensure symmetry
    for i in range(n):
        for j in range(i, n):  # Only process upper triangle and diagonal
            if i == j:
                # Self-loops: keep if exists in directed graph
                Aundir[i][j] = Adir[i][j]
            else:
                # Regular edges: if there's an edge in either direction, add undirected edge
                if Adir[i][j] == 1 or Adir[j][i] == 1:
                    Aundir[i][j] = 1
                    Aundir[j][i] = 1  # Make symmetric
    
    return Aundir

def matrix_multiply(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    """Multiply two matrices"""
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

def matrix_power(matrix: list[list[int]], power: int) -> list[list[int]]:
    """Calculate matrix to the given power"""
    n = len(matrix)
    if power == 1:
        return [row[:] for row in matrix]  # Copy matrix
    
    result = matrix_power(matrix, power - 1)
    return matrix_multiply(matrix, result)

def calculate_grid_size(n: int) -> tuple[int, int]:
    """Calculate optimal grid size for vertex positioning"""
    grid_size = math.ceil(math.sqrt(n))
    return grid_size, grid_size