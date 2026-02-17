"""
AI Pathfinder - Uninformed Search Algorithms
Implements: BFS, DFS, UCS, DLS, IDDFS, and Bidirectional Search
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from collections import deque
import heapq
import random

class GridWorld:
    """Grid environment with static walls"""
    
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols))
        self.start = None
        self.target = None
        
    def set_start(self, row, col):
        """Set starting position"""
        self.start = (row, col)
        
    def set_target(self, row, col):
        """Set target position"""
        self.target = (row, col)
        
    def add_wall(self, row, col):
        """Add static wall"""
        self.grid[row, col] = -1
        
    def add_random_walls(self, num_walls):
        """Add random static walls"""
        count = 0
        while count < num_walls:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if (row, col) != self.start and (row, col) != self.target and self.grid[row, col] == 0:
                self.grid[row, col] = -1
                count += 1
    

    
    def is_valid(self, row, col):
        """Check if position is valid and not a wall"""
        return (0 <= row < self.rows and 0 <= col < self.cols and self.grid[row, col] != -1)
    
    def get_neighbors(self, node):
        """Get valid neighbors excluding top-right and bottom-left diagonals"""
        row, col = node
        directions = [(-1, 0), (0, 1), (1, 1), (1, 0), (0, -1), (-1, -1)]
        neighbors = []
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_valid(new_row, new_col):
                cost = 1.414 if (dr != 0 and dc != 0) else 1.0
                neighbors.append(((new_row, new_col), cost))
        return neighbors


class SearchVisualizer:
    """Visualize search algorithms step by step"""
    
    def __init__(self, grid_world):
        self.grid_world = grid_world
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.fig.suptitle('Visual', fontsize=14, fontweight='bold')
        self.explored = set()
        self.frontier = set()
        self.path = []
        self.current_node = None
        
    def setup_plot(self, title):
        """Initialize the plot"""
        self.ax.clear()
        self.ax.set_xlim(-0.5, self.grid_world.cols - 0.5)
        self.ax.set_ylim(-0.5, self.grid_world.rows - 0.5)
        self.ax.set_aspect('equal')
        self.ax.set_title(title, fontsize=16, fontweight='bold')
        self.ax.set_xticks(range(self.grid_world.cols))
        self.ax.set_yticks(range(self.grid_world.rows))
        self.ax.grid(True, linewidth=0.5, alpha=0.3)
        self.ax.invert_yaxis()
    
    def _draw_rectangle(self, row, col, color, edge_color='gray', alpha=0.6, linewidth=1, edge_width=None):
        """Helper to draw a rectangle at given position"""
        if edge_width is None:
            edge_width = linewidth
        rect = patches.Rectangle((col - 0.5, row - 0.5), 1, 1,
                                linewidth=edge_width, edgecolor=edge_color,
                                facecolor=color, alpha=alpha)
        self.ax.add_patch(rect)
        
    def draw_grid(self):
        """Draw the current state of the grid"""
        # Draw walls
        for i in range(self.grid_world.rows):
            for j in range(self.grid_world.cols):
                if self.grid_world.grid[i, j] == -1:
                    self._draw_rectangle(i, j, 'black', 'black')
        
        # Draw explored nodes
        for node in self.explored:
            if node not in [self.grid_world.start, self.grid_world.target]:
                self._draw_rectangle(node[0], node[1], 'lightblue', 'gray')
        
        # Draw frontier nodes
        for node in self.frontier:
            if node not in [self.grid_world.start, self.grid_world.target]:
                self._draw_rectangle(node[0], node[1], 'yellow', 'orange', alpha=0.7)
        
        # Draw current node
        if self.current_node and self.current_node not in [self.grid_world.start, self.grid_world.target]:
            self._draw_rectangle(self.current_node[0], self.current_node[1], 'violet', 'purple', alpha=0.8, linewidth=2)
        
        # Draw path
        for node in self.path:
            if node not in [self.grid_world.start, self.grid_world.target]:
                self._draw_rectangle(node[0], node[1], 'lightgreen', 'green', alpha=0.9, linewidth=2)
        
        # Draw start position
        if self.grid_world.start:
            self._draw_rectangle(self.grid_world.start[0], self.grid_world.start[1], 'blue', 'blue', alpha=0.8, linewidth=2)
            self.ax.text(self.grid_world.start[1], self.grid_world.start[0], 'S',
                        ha='center', va='center', fontsize=20, fontweight='bold', color='white')
        
        # Draw target position
        if self.grid_world.target:
            self._draw_rectangle(self.grid_world.target[0], self.grid_world.target[1], 'green', 'red', alpha=0.8, linewidth=2)
            self.ax.text(self.grid_world.target[1], self.grid_world.target[0], 'T',
                        ha='center', va='center', fontsize=20, fontweight='bold', color='white')
        
        # Add legend
        legend_elements = [
            patches.Patch(facecolor='blue', label='Start (S)'),
            patches.Patch(facecolor='green', label='Target (T)'),
            patches.Patch(facecolor='black', label='Static Wall'),
            patches.Patch(facecolor='yellow', label='Frontier'),
            patches.Patch(facecolor='lightblue', label='Explored'),
            patches.Patch(facecolor='violet', label='Current Node'),
            patches.Patch(facecolor='lightgreen', label='Final Path')
        ]
        self.ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))
        plt.tight_layout()


class PathFinder:
    """Implements various uninformed search algorithms"""
    
    def __init__(self, grid_world, visualizer=None, delay=0.1):
        self.grid_world = grid_world
        self.visualizer = visualizer
        self.delay = delay
        
    def reconstruct_path(self, came_from, current):
        """Reconstruct path from start to target"""
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path
    
    def _generic_search(self, use_stack=False, use_priority=False, depth_limit=None, title=None):
        """Generic search framework for BFS, DFS, DLS, and UCS"""
        if self.visualizer and title:
            self.visualizer.setup_plot(title)
        
        start = self.grid_world.start
        target = self.grid_world.target
        
        # Initialize container based on algorithm type
        if use_priority:
            container = [(0, start)]
            cost_so_far = {start: 0}
        else:
            container = deque([start]) if not use_stack else [start]
            cost_so_far = {start: 0}  # Track cost for all algorithms
        
        came_from = {}
        explored = set()
        
        while container:
            # Pop from container based on type
            if use_priority:
                current_cost, current = heapq.heappop(container)
            elif use_stack:
                current = container.pop()
            else:
                current = container.popleft()
            
            if current == target:
                path = self.reconstruct_path(came_from, current)
                if self.visualizer:
                    self.visualizer.path = path
                    self.visualizer.draw_grid()
                    plt.pause(0.5)
                return path, len(explored), cost_so_far[current]
            
            if current in explored:
                continue
            
            explored.add(current)
            
            # Visualize
            if self.visualizer:
                self.visualizer.current_node = current
                self.visualizer.explored = explored.copy()
                if use_priority:
                    self.visualizer.frontier = {node for _, node in container}
                else:
                    self.visualizer.frontier = set(container)
                self.visualizer.draw_grid()
                plt.pause(self.delay)
            
            # Expand neighbors
            for neighbor, move_cost in self.grid_world.get_neighbors(current):
                if neighbor in explored:
                    continue
                
                # Check depth limit for DLS
                if depth_limit is not None:
                    depth = len(self.reconstruct_path(came_from, current)) + 1
                    if depth > depth_limit:
                        continue
                
                new_cost = cost_so_far[current] + move_cost
                
                # Add to cost_so_far if not already there or if we found a cheaper path
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    
                    if neighbor not in came_from:
                        came_from[neighbor] = current
                    
                    if use_priority:
                        heapq.heappush(container, (new_cost, neighbor))
                    else:
                        if use_stack:
                            container.append(neighbor)
                        else:
                            container.append(neighbor)
        
        return None, len(explored), 0
    
    
    def bfs(self):
        """Breadth-First Search"""
        return self._generic_search(use_stack=False, title="Breadth-First Search (BFS)")
    
    def dfs(self):
        """Depth-First Search"""
        return self._generic_search(use_stack=True, title="Depth-First Search (DFS)")
    
    def ucs(self):
        """Uniform-Cost Search"""
        return self._generic_search(use_priority=True, title="Uniform-Cost Search (UCS)")
    
    def dls(self, depth_limit=5):
        """Depth-Limited Search"""
        return self._generic_search(use_stack=True, depth_limit=depth_limit, 
                                   title=f"Depth-Limited Search (DLS) - Limit: {depth_limit}")
    
    def iddfs(self, max_depth=10):
        """Iterative Deepening DFS"""
        if self.visualizer:
            self.visualizer.setup_plot("Iterative Deepening DFS (IDDFS)")
        
        for depth_limit in range(max_depth + 1):
            path, _, cost = self.dls(depth_limit)
            if path is not None:
                return path, 0, cost
        
        return None, 0, 0
    
    def bidirectional_search(self):
        """Bidirectional Search"""
        if self.visualizer:
            self.visualizer.setup_plot("Bidirectional Search")
        
        start = self.grid_world.start
        target = self.grid_world.target
        
        queue_forward = deque([start])
        came_from_forward = {start: None}
        explored_forward = set()
        cost_forward = {start: 0}
        
        queue_backward = deque([target])
        came_from_backward = {target: None}
        explored_backward = set()
        cost_backward = {target: 0}
        
        while queue_forward and queue_backward:
            # Expand forward
            if queue_forward:
                current_forward = queue_forward.popleft()
                explored_forward.add(current_forward)
                
                if current_forward in explored_backward:
                    path = self._construct_bidirectional_path(came_from_forward, came_from_backward, current_forward)
                    total_cost = cost_forward[current_forward] + cost_backward[current_forward]
                    if self.visualizer:
                        self.visualizer.path = path
                        self.visualizer.draw_grid()
                        plt.pause(0.5)
                    return path, len(explored_forward) + len(explored_backward), total_cost
                
                for neighbor, move_cost in self.grid_world.get_neighbors(current_forward):
                    if neighbor not in explored_forward and neighbor not in came_from_forward:
                        queue_forward.append(neighbor)
                        came_from_forward[neighbor] = current_forward
                        cost_forward[neighbor] = cost_forward[current_forward] + move_cost
            
            # Expand backward
            if queue_backward:
                current_backward = queue_backward.popleft()
                explored_backward.add(current_backward)
                
                if current_backward in explored_forward:
                    path = self._construct_bidirectional_path(came_from_forward, came_from_backward, current_backward)
                    total_cost = cost_forward[current_backward] + cost_backward[current_backward]
                    if self.visualizer:
                        self.visualizer.path = path
                        self.visualizer.draw_grid()
                        plt.pause(0.5)
                    return path, len(explored_forward) + len(explored_backward), total_cost
                
                for neighbor, move_cost in self.grid_world.get_neighbors(current_backward):
                    if neighbor not in explored_backward and neighbor not in came_from_backward:
                        queue_backward.append(neighbor)
                        came_from_backward[neighbor] = current_backward
                        cost_backward[neighbor] = cost_backward[current_backward] + move_cost
            
            # Visualize
            if self.visualizer:
                self.visualizer.explored = explored_forward.union(explored_backward)
                self.visualizer.frontier = set(queue_forward).union(set(queue_backward))
                self.visualizer.draw_grid()
                plt.pause(self.delay)
        
        return None, len(explored_forward) + len(explored_backward), 0
    
    def _construct_bidirectional_path(self, came_from_forward, came_from_backward, meeting_point):
        """Construct path for bidirectional search"""
        path_forward = []
        current = meeting_point
        while current is not None:
            path_forward.append(current)
            current = came_from_forward[current]
        path_forward.reverse()
        
        path_backward = []
        current = came_from_backward[meeting_point]
        while current is not None:
            path_backward.append(current)
            current = came_from_backward[current]
        
        return path_forward + path_backward


def run_algorithm(algorithm_name, grid_world, delay=0.1):
    """Run a specific algorithm and visualize it"""
    visualizer = SearchVisualizer(grid_world)
    pathfinder = PathFinder(grid_world, visualizer, delay)
    
    print(f"\nRunning {algorithm_name}...")
    
    algorithm_map = {
        "BFS": pathfinder.bfs,
        "DFS": pathfinder.dfs,
        "UCS": pathfinder.ucs,
        "DLS": lambda: pathfinder.dls(depth_limit=8),
        "IDDFS": lambda: pathfinder.iddfs(max_depth=15),
        "Bidirectional": pathfinder.bidirectional_search
    }
    
    if algorithm_name not in algorithm_map:
        print(f"Unknown algorithm: {algorithm_name}")
        return
    
    path, nodes_explored, cost = algorithm_map[algorithm_name]()
    
    if path:
        print(f"✓ Path found!")
        print(f"  - Path Length: {len(path)}")
        print(f"  - Total Cost: {cost:.3f}")
        print(f"  - Nodes Discovered: {nodes_explored}")
    else:
        print(f"✗ No path found. Nodes explored: {nodes_explored}")
    
    plt.show()


def create_grid(scenario):
    """Create grid based on scenario selection"""
    if scenario == "1":
        # Best Case: Clear path
        grid = GridWorld(10, 10)
        grid.set_start(1, 1)
        grid.set_target(8, 8)
        for i in range(3, 7):
            grid.add_wall(5, i)
    elif scenario == "2":
        # Worst Case: Complex maze
        grid = GridWorld(10, 10)
        grid.set_start(1, 1)
        grid.set_target(8, 8)
        grid.add_random_walls(25)
    else:
        # Custom: Medium complexity
        grid = GridWorld(10, 10)
        grid.set_start(1, 1)
        grid.set_target(8, 8)
        grid.add_random_walls(15)
    
    return grid


def main():
    """Main function to run the pathfinder"""
    print("=" * 60)
    print("AI PATHFINDER - Uninformed Search Algorithms")
    print("=" * 60)
    
    # Choose scenario
    print("\nSelect Scenario:")
    print("1. Best Case (Clear path)")
    print("2. Worst Case (Complex maze)")
    print("3. Custom Grid")
    
    scenario = input("Enter choice (1-3): ").strip()
    grid = create_grid(scenario)
    
    algorithms = ["BFS", "DFS", "UCS", "DLS", "IDDFS", "Bidirectional"]
    
    # Choose algorithm - loop for multiple runs
    while True:
        print("\nSelect Algorithm:")
        for i, algo in enumerate(algorithms, 1):
            print(f"{i}. {algo}")
        print("7. Run All Algorithms")
        print("8. Exit")

        algo_choice = input("Enter choice (1-8): ").strip()
        
        if algo_choice == "8":
            print("Exiting program...")
            break
        
        if algo_choice == "7":
            for algo in algorithms:
                grid = create_grid(scenario)
                run_algorithm(algo, grid, delay=0.05)
        elif algo_choice == "4":  # DLS selected
            while True:
                try:
                    depth_limit = int(input("Enter depth limit (1-20): ").strip())
                    if 1 <= depth_limit <= 20:
                        visualizer = SearchVisualizer(grid)
                        pathfinder = PathFinder(grid, visualizer, 0.1)
                        
                        print(f"\nRunning DLS with depth limit {depth_limit}...")
                        path, nodes_explored, cost = pathfinder.dls(depth_limit=depth_limit)
                        
                        if path:
                            print(f"✓ Path found!")
                            print(f"  - Path Length: {len(path)}")
                            print(f"  - Total Cost: {cost:.3f}")
                            print(f"  - Nodes Discovered: {nodes_explored}")
                        else:
                            print(f"✗ No path found. Nodes explored: {nodes_explored}")
                        
                        plt.show()
                        break
                    else:
                        print("Invalid input! Please enter a number between 1 and 20.")
                except ValueError:
                    print("Invalid input! Please enter a valid integer.")
        elif algo_choice.isdigit() and 1 <= int(algo_choice) <= 6:
            run_algorithm(algorithms[int(algo_choice) - 1], grid, delay=0.1)
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
