"""
Configuration module for Laboratory Work 4
Contains all input parameters and constants
"""

# Input parameters
N1, N2, N3, N4 = 4, 1, 3, 2
N = 10 + N3  # 13 vertices
SEED = int(f"{N1}{N2}{N3}{N4}")

# Two different k coefficients for different parts
K1 = 1.0 - N3 * 0.01 - N4 * 0.01 - 0.3  # For first part
K2 = 1.0 - N3 * 0.005 - N4 * 0.005 - 0.27  # For second part

# Grid configuration
import math
GRID_SIZE = math.ceil(math.sqrt(N))
ROWS, COLS = GRID_SIZE, GRID_SIZE

# UI constants
CANVAS_SIZE = 600
MARGIN = 50
NODE_RADIUS = 15