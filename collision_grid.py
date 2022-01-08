import math

class CollisionGrid() :

    def __init__(self, grid_size, width, height) :
        self.grid_size = grid_size
        self.width = width
        self.height = height
        self.grid_width = int(math.ceil(width / float(grid_size)))
        self.grid_height = int(math.ceil(height / float(grid_size)))
        self.collision_grid = [[] for i in range(self.grid_width * self.grid_height)]

    def reset_grid(self) :
        for i in range(0, self.grid_width * self.grid_height) :
            self.collision_grid[i].clear()

    def add_to_grid(self, rb) :
        grid_pos = self.make_grid_coord(rb.pos_f)
        for i in range(-rb.grid_size, rb.grid_size + 1) :
            for j in range(-rb.grid_size, rb.grid_size + 1) :
                x = grid_pos[0] + i
                y = grid_pos[1] = j
                if x >= 0 and x < self.grid_width and y >= 0 and y < self.grid_height :
                    self.collision_grid[x * self.grid_height + y].append(rb)

    def make_grid_coord(self, pos_f) :
        return [int(pos_f[0] / self.grid_size), int(pos_f[1] / self.grid_size)]

    def check_all(self, resolve) :
        for i in range(self.grid_width) :
            for j in range(self.grid_height) :
                checks = self.collision_grid[i * self.grid_height + j]
                for rb1 in range(len(checks)) :
                    for rb2 in range(rb1 + 1, len(checks)) :
                        collided, heading = checks[rb1].collision_test(checks[rb2])
                        if collided :
                            checks[rb1].collision_enter(checks[rb2])
                            checks[rb2].collision_enter(rb1)
                            if resolve:
                                checks[rb1].solve_collision(checks[rb2], heading)

