import pygame
import sys
import numpy as np
import random
from collision_grid import CollisionGrid
from rigidbody import RigidBody
import common_vars as cv

def main():
    pygame.init()
    clock  = pygame.time.Clock()
    fps = 30
    bg = [255, 255, 255]
    size = [cv.WIDTH, cv.HEIGHT]

    screen = pygame.display.set_mode(size)

    loop = True

    rb_group = pygame.sprite.Group()
    max_vel = 100
    col_grid = CollisionGrid(cv.GRID_SIZE, cv.WIDTH, cv.HEIGHT)

    for i in range(150) :
        pos = [random.randint(0, cv.WIDTH), random.randint(0, cv.HEIGHT)] 
        vel = [(random.random() - 0.5) * max_vel * 2 for _ in range(2)]
        pushable = random.random() < 0.9
        grid_size = random.random() + 0.5
        if random.random() > 0.9:
            grid_size += 1
            if random.random() > 0.9:
                grid_size += 1
        rb_group.add(RigidBody(pos, vel, pushable, grid_size))

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
        screen.fill(bg)

        rb_group.update()
       
        col_grid.reset_grid()
        for rb in rb_group.sprites():
            col_grid.add_to_grid(rb)
        col_grid.check_all(True)

        rb_group.draw(screen)
        pygame.display.update()
        cv.dTime = clock.tick(fps) / 1000.
        # print(cv.dTime)

    pygame.quit()

if __name__ == '__main__':
    main()
