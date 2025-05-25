"""
Graph Visualizer Module
Handles graph drawing, smart routing, and visual representation
"""
import tkinter as tk
import math

class GraphVisualizer:
    def __init__(self, canvas, canvas_size=600, margin=50, node_radius=15):
        self.canvas = canvas
        self.canvas_size = canvas_size
        self.margin = margin
        self.node_radius = node_radius
        self.positions = []
    
    def calculate_positions(self, n, rows, cols):
        """Calculate vertex positions in grid layout"""
        self.positions = []
        count = 0
        for r in range(rows):
            for c in range(cols):
                if count < n:
                    x = self.margin + c * ((self.canvas_size - 2 * self.margin) / max(1, cols - 1))
                    y = self.margin + r * ((self.canvas_size - 2 * self.margin) / max(1, rows - 1))
                    self.positions.append((x, y))
                    count += 1
    
    def point_distance(self, x1, y1, x2, y2):
        """Calculate distance between two points"""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def line_circle_distance(self, x1, y1, x2, y2, cx, cy):
        """Calculate minimum distance from a line segment to a circle center"""
        # Vector from start to end
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0 and dy == 0:
            return self.point_distance(x1, y1, cx, cy)
        
        # Parameter t for the closest point on the line
        t = max(0, min(1, ((cx - x1) * dx + (cy - y1) * dy) / (dx * dx + dy * dy)))
        
        # Closest point on the line segment
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        
        return self.point_distance(closest_x, closest_y, cx, cy)
    
    def find_best_path(self, start_pos, end_pos, all_positions):
        """Find the best path between two nodes avoiding other nodes"""
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Direct path
        direct_distance = self.point_distance(x1, y1, x2, y2)
        if direct_distance == 0:
            return start_pos, end_pos
        
        # Check if direct path intersects with other nodes
        path_clear = True
        for pos in all_positions:
            if pos == start_pos or pos == end_pos:
                continue
            
            px, py = pos
            # Check if the line from start to end passes too close to this node
            if self.line_circle_distance(x1, y1, x2, y2, px, py) < self.node_radius + 8:
                path_clear = False
                break
        
        if path_clear:
            # Direct path is clear, just adjust for node radius
            dx = x2 - x1
            dy = y2 - y1
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                unit_x = dx / length
                unit_y = dy / length
                start_x = x1 + unit_x * self.node_radius
                start_y = y1 + unit_y * self.node_radius
                end_x = x2 - unit_x * self.node_radius
                end_y = y2 - unit_y * self.node_radius
                return (start_x, start_y), (end_x, end_y)
        
        # If direct path is blocked, try curved path
        return self.create_curved_path(start_pos, end_pos, all_positions)
    
    def create_curved_path(self, start_pos, end_pos, all_positions):
        """Create a curved path that avoids other nodes"""
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Calculate midpoint
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # Calculate perpendicular offset
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        
        if length == 0:
            return start_pos, end_pos
        
        # Perpendicular vector
        perp_x = -dy / length
        perp_y = dx / length
        
        # Try different curve offsets
        for offset in [25, 40, 60, 80]:
            for direction in [1, -1]:  # Try both sides
                curve_x = mid_x + perp_x * offset * direction
                curve_y = mid_y + perp_y * offset * direction
                
                # Check if this curved path avoids other nodes
                path_clear = True
                for pos in all_positions:
                    if pos == start_pos or pos == end_pos:
                        continue
                    
                    px, py = pos
                    # Check distance to both segments of the curve
                    dist1 = self.line_circle_distance(x1, y1, curve_x, curve_y, px, py)
                    dist2 = self.line_circle_distance(curve_x, curve_y, x2, y2, px, py)
                    
                    if dist1 < self.node_radius + 8 or dist2 < self.node_radius + 8:
                        path_clear = False
                        break
                
                if path_clear:
                    # Adjust for node radius
                    dx1 = curve_x - x1
                    dy1 = curve_y - y1
                    length1 = math.sqrt(dx1*dx1 + dy1*dy1)
                    if length1 > 0:
                        unit_x1 = dx1 / length1
                        unit_y1 = dy1 / length1
                        start_x = x1 + unit_x1 * self.node_radius
                        start_y = y1 + unit_y1 * self.node_radius
                    else:
                        start_x, start_y = x1, y1
                    
                    dx2 = x2 - curve_x
                    dy2 = y2 - curve_y
                    length2 = math.sqrt(dx2*dx2 + dy2*dy2)
                    if length2 > 0:
                        unit_x2 = dx2 / length2
                        unit_y2 = dy2 / length2
                        end_x = x2 - unit_x2 * self.node_radius
                        end_y = y2 - unit_y2 * self.node_radius
                    else:
                        end_x, end_y = x2, y2
                    
                    return (start_x, start_y), (end_x, end_y), (curve_x, curve_y)
        
        # Fallback to direct path with node radius adjustment
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            unit_x = dx / length
            unit_y = dy / length
            start_x = x1 + unit_x * self.node_radius
            start_y = y1 + unit_y * self.node_radius
            end_x = x2 - unit_x * self.node_radius
            end_y = y2 - unit_y * self.node_radius
            return (start_x, start_y), (end_x, end_y)
        
        return start_pos, end_pos
    
    def draw_smart_line(self, start_pos, end_pos, with_arrow=False):
        """Draw a line with smart routing to avoid other nodes"""
        path_result = self.find_best_path(start_pos, end_pos, self.positions)
        
        if len(path_result) == 3:
            # Curved path
            start_pos, end_pos, curve_point = path_result
            x1, y1 = start_pos
            cx, cy = curve_point
            x2, y2 = end_pos
            
            # Draw the curve as two line segments
            self.canvas.create_line(x1, y1, cx, cy, fill="black", width=2)
            if with_arrow:
                self.canvas.create_line(cx, cy, x2, y2, fill="black", width=2, 
                                      arrow=tk.LAST, arrowshape=(10, 12, 3))
            else:
                self.canvas.create_line(cx, cy, x2, y2, fill="black", width=2)
        else:
            # Straight path
            start_pos, end_pos = path_result
            x1, y1 = start_pos
            x2, y2 = end_pos
            if with_arrow:
                self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2, 
                                      arrow=tk.LAST, arrowshape=(10, 12, 3))
            else:
                self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
    
    def draw_self_loop(self, x, y, with_arrow=False):
        """Draw a self-loop at given position"""
        r = self.node_radius
        self.canvas.create_oval(x + r, y - r * 1.5, x - 2*r, y - r * 0.5, 
                              outline="black", width=2)
        if with_arrow:
            self.canvas.create_line(x + r/2, y - r * 1.5, x + r/2 + 5, y - r * 1.5 - 5, 
                                  fill="black", width=2, arrow=tk.LAST, arrowshape=(8, 10, 3))
    
    def draw_node(self, x, y, label, color="lightblue"):
        """Draw a single node"""
        r = self.node_radius
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="black", width=2)
        self.canvas.create_text(x, y, text=label, font=("Arial", 10, "bold"))
    
    def get_condensation_positions(self, num_components):
        """Calculate positions for condensation graph"""
        positions = []
        if num_components <= 4:
            # Arrange in a line
            for i in range(num_components):
                x = self.margin + i * ((self.canvas_size - 2 * self.margin) / max(1, num_components - 1))
                y = self.canvas_size // 2
                positions.append((x, y))
        else:
            # Arrange in a circle
            center_x, center_y = self.canvas_size // 2, self.canvas_size // 2
            radius = min(self.canvas_size // 3, 200)
            for i in range(num_components):
                angle = 2 * math.pi * i / num_components
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                positions.append((x, y))
        return positions
    
    def clear_canvas(self):
        """Clear the canvas"""
        self.canvas.delete("all")