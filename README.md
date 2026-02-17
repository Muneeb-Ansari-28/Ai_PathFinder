# AI Pathfinder - Uninformed Search Algorithms

A comprehensive implementation of six uninformed search algorithms with "Visual" GUI visualization.

## 📋 Table of Contents
- [Features](#features)
- [Algorithms Implemented](#algorithms-implemented)
- [Installation](#installation)
- [Usage](#usage)
- [Algorithm Details](#algorithm-details)
- [Visualization](#visualization)
- [Project Structure](#project-structure)

## ✨ Features

✅ **Six Search Algorithms**: BFS, DFS, UCS, DLS, IDDFS, Bidirectional Search  
✅ **Real-time Visual GUI**: Watch algorithms explore the grid step-by-step  
✅ **6-Directional Movement**: Up, Down, Left, Right, and two diagonal movements  
✅ **Comprehensive Statistics**: Path length, nodes explored, execution cost  
✅ **Best/Worst Case Testing**: Pre-configured scenarios for analysis  

## 🔍 Algorithms Implemented

### 1. Breadth-First Search (BFS)
- **Strategy**: Explores level by level
- **Data Structure**: Queue (FIFO)
- **Completeness**: ✓ Complete
- **Optimality**: ✓ Optimal for unweighted graphs
- **Best For**: Finding shortest path in unweighted grids

### 2. Depth-First Search (DFS)
- **Strategy**: Explores as deep as possible before backtracking
- **Data Structure**: Stack (LIFO)
- **Completeness**: ✓ Complete (in finite spaces)
- **Optimality**: ✗ Not optimal
- **Best For**: When memory is limited

### 3. Uniform-Cost Search (UCS)
- **Strategy**: Expands nodes with lowest path cost
- **Data Structure**: Priority Queue
- **Completeness**: ✓ Complete
- **Optimality**: ✓ Optimal
- **Best For**: Weighted grids with different movement costs

### 4. Depth-Limited Search (DLS)
- **Strategy**: DFS with depth constraint
- **Data Structure**: Stack with depth tracking
- **Completeness**: ✗ Not complete (if limit too low)
- **Optimality**: ✗ Not optimal
- **Best For**: When maximum solution depth is known

### 5. Iterative Deepening DFS (IDDFS)
- **Strategy**: Runs DLS with increasing depth limits
- **Data Structure**: Stack (multiple iterations)
- **Completeness**: ✓ Complete
- **Optimality**: ✓ Optimal (unweighted)
- **Best For**: When depth is unknown and memory is limited

### 6. Bidirectional Search
- **Strategy**: Search from both start and goal simultaneously
- **Data Structure**: Two queues
- **Completeness**: ✓ Complete
- **Optimality**: ✓ Optimal
- **Best For**: When both start and goal are known

## 🚀 Installation

### Prerequisites
```bash
python >= 3.7
```

### Required Libraries
```bash
pip install matplotlib numpy
```

### Quick Start
```bash
# Clone or download the files
# Run the main program
python finder.py


## 💻 Usage

### Interactive Mode
```bash
python finder.py
```

Follow the prompts to:
1. Choose scenario (Best Case / Worst Case / Custom)
2. Select algorithm
3. Watch the visualization

### Programmatic Usage
```python
from finder import GridWorld, PathFinder, SearchVisualizer

# Create grid
grid = GridWorld(10, 10)
grid.set_start(1, 1)
grid.set_target(8, 8)
grid.add_random_walls(15)

# Setup visualization
visualizer = SearchVisualizer(grid)
pathfinder = PathFinder(grid, visualizer, delay=0.1)

# Run algorithm
path, nodes_explored, cost = pathfinder.bfs()

# Show result
import matplotlib.pyplot as plt
plt.show()
```

## 🎨 Visualization

### Color Legend
- 🟦 **Blue**: Start position (S)
- 🟩 **Green**: Target position (T)
- ⬛ **Black**: Static walls
-  **Yellow**: Frontier nodes (waiting to be explored)
- 🟦 **Light Blue**: Explored nodes
- 🟪 **Violet**: Current node being processed
- 🟩 **Light Green**: Final path

### Movement Order
Neighbors are checked in the following order (6 directions - excluding top-right and bottom-left diagonals):
1. Up (-1, 0)
2. Right (0, 1)
3. Down-Right (1, 1) - Diagonal
4. Down (1, 0)
5. Left (0, -1)
6. Top-Left (-1, -1) - Diagonal

**Movement Costs**:
- Straight moves: 1.0
- Diagonal moves: √2 ≈ 1.414

## 📁 Project Structure

```
ai-pathfinder/
├── finder.py      # Main implementation
├── README.md            # This file
```

## 📊 Algorithm Comparison

### Time Complexity
| Algorithm | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| BFS | O(b^d) | O(b^d) |
| DFS | O(b^m) | O(bm) |
| UCS | O(b^(1+C*/ε)) | O(b^(1+C*/ε)) |
| DLS | O(b^l) | O(bl) |
| IDDFS | O(b^d) | O(bd) |
| Bidirectional | O(b^(d/2)) | O(b^(d/2)) |

*Where: b=branching factor, d=depth of solution, m=maximum depth, l=depth limit, C*=optimal cost, ε=minimum cost*

### Pros and Cons

#### BFS
**Pros**:
- Guarantees shortest path
- Simple to implement
- Explores systematically

**Cons**:
- High memory usage
- Slow on large grids
- Explores many unnecessary nodes

#### DFS
**Pros**:
- Low memory usage
- Fast in some cases
- Good for deep solutions

**Cons**:
- Not optimal
- Can get stuck in deep paths
- May miss shorter solutions

#### UCS
**Pros**:
- Optimal for weighted graphs
- Handles variable costs
- Always finds cheapest path

**Cons**:
- Higher memory than DFS
- Slower than BFS on unweighted
- More complex implementation

#### DLS
**Pros**:
- Memory efficient
- Prevents infinite loops
- Fast if limit is correct

**Cons**:
- Not complete
- Fails if limit too low
- Not optimal

#### IDDFS
**Pros**:
- Optimal like BFS
- Memory efficient like DFS
- Complete search

**Cons**:
- Redundant node expansions
- Slower than BFS
- Multiple iterations needed

#### Bidirectional
**Pros**:
- Fastest when applicable
- Significantly reduces search space
- Optimal

**Cons**:
- Needs known goal
- More complex
- Higher implementation overhead

## 📊 Testing Scenarios

### Best Case
- Clear, direct path from start to goal
- Minimal obstacles
- Algorithms should find solution quickly
- Expected: BFS/UCS find optimal path

### Worst Case
- Complex maze with many walls
- Long, winding required path
- Algorithms explore extensively
- Expected: DFS may explore entire grid, BFS guarantees shortest

## 🔧 Customization

### Grid Size
```python
grid = GridWorld(rows=15, cols=15)
```

### Obstacle Density
```python
grid.add_random_walls(num_walls=30)
```

### Animation Speed
```python
finder = PathFinder(grid, visualizer, delay=0.05)  # 50ms delay
```

### Depth Limits
```python
path, nodes = finder.dls(depth_limit=12)
path, nodes = finder.iddfs(max_depth=20)
```
