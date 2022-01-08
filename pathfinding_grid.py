import math
from queue import PriorityQueue
from itertools import count
import time
import random

#TODO: consolidate this with the collision grid

#pathfinding cost no be this big
BIGNUMBER = 99999999

class GridNode():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.can_path = True
        self.cost = 1.
        self.last_parent = None

    def heuristic(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def __str__(self):
        return f'({self.x}, {self.y})'

class PathfindingGrid():

    def __init__(self, grid_size, width, height):
        self.grid_size = grid_size
        self.width = width
        self.height = height
        self.grid_width = int(math.ceil(width / float(grid_size)))
        self.grid_height = int(math.ceil(height / float(grid_size)))
        self.grid = [GridNode(i // self.grid_height, i % self.grid_height) for i in range(self.grid_width * self.grid_height)]

    def reset_grid(self):
        for n in self.grid:
            n.last_cost = BIGNUMBER
    
    def solve_path(self, start_x, start_y, end_x, end_y):
        queue_count = count()
        self.reset_grid()
        queue = PriorityQueue()
        current = self.get_grid(start_x, start_y)
        goal = self.get_grid(end_x, end_y)
        current.last_parent = None
        current.last_cost = current.cost
        while current != goal:
            #print(current)
            neighbors = self.get_neighbors(current.x, current.y)
            for n in neighbors: 
                if n == goal:
                    print(f'visited {queue_count}')
                    n.last_parent = current
                    return self.unwind_path(n)
                elif n.can_path and n.last_cost > current.last_cost + n.cost:
                    n.last_parent = current
                    n.last_cost = current.last_cost + n.cost
                    queue.put((n.last_cost + n.heuristic(goal), next(queue_count), n))
            if queue.empty():
                return []
            current = queue.get()[2]

    def unwind_path(self, last_node):
        n = last_node
        res = [last_node]
        while(n.last_parent != None):
            n = n.last_parent
            res.insert(0, n)
        return res
        
            
    def get_neighbors(self, x, y):
        res = []
        if x > 0:
            res.append(self.get_grid(x - 1, y))
        if y > 0:
            res.append(self.get_grid(x, y - 1))
        if x < self.grid_width - 1:
            res.append(self.get_grid(x + 1, y))
        if y < self.grid_height - 1:
            res.append(self.get_grid(x, y + 1))
        return res

    def block_spot(self, x, y):
        self.get_grid(x, y).can_path = False

    def set_cost(self, x, y, cost):
        self.get_grid(x, y).cost = cost

    def get_grid(self, x, y):
        return self.grid[x * self.grid_height + y]

        
def run_test(grid, x, y, x2, y2):
    start = time.time()
    res = grid.solve_path(x, y, x2, y2)
    end = time.time()
    print(f'Path Length: {len(res)}, {(end-start)*1000}ms')
    print(' '.join(str(g) for g in res))
    print('------------')

if __name__ == '__main__': 
    test_grid = PathfindingGrid(20, 600, 600)
    run_test(test_grid, 0, 0, 20, 20)
    
    for i in range(2, 10):
        test_grid.block_spot(i, 3)
    run_test(test_grid, 0, 0, 20, 20)
    

    for i in range(16, 25):
        test_grid.block_spot(i, 17)
    run_test(test_grid, 0, 0, 20, 20)

    for i in range(0, len(test_grid.grid)):
        if(random.random() < 0.3):
            test_grid.grid[i].can_path = False
    run_test(test_grid, 0, 0, 20, 20)
    
