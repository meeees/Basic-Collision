import numpy as np
import pygame
import common_vars as cv

class RigidBody(pygame.sprite.Sprite):
    def __init__(self, pos, vel, pushable, grid_size=1):
        pygame.sprite.Sprite.__init__(self)
        # grid size is a whole number, minimum 1 (for collision grid)
        self.grid_size = 1 if grid_size < 1 else int(np.floor(grid_size))
        self.diameter = grid_size * cv.GRID_SIZE
        self.radius = self.diameter / 2

        self.normal_image = pygame.Surface([self.diameter, self.diameter], pygame.SRCALPHA)
        self.collision_image = pygame.Surface([self.diameter, self.diameter], pygame.SRCALPHA)
        color = (255, 0, 0) if pushable else (0, 0, 255)
        collide_color = (0, 255, 0) if pushable else (0, 128, 0)
        pygame.draw.circle(self.normal_image, color, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.collision_image, collide_color, (self.radius, self.radius), self.radius)
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.vel = np.array(vel) / grid_size
        self.pos_f =  np.array([float(pos[0]), float(pos[1])])
        self.can_be_pushed = pushable
        self.collisions = set()

    def update(self):
        # TODO optimize this to not suck
        if len(self.collisions) > 0:
            self.image = self.normal_image
        self.collisions.clear()

        self.pos_f += self.vel * cv.dTime
        if self.pos_f[0] < 0:
            self.vel[0] = np.abs(self.vel[0])
        if self.pos_f[0] > cv.WIDTH:
            self.vel[0] = -np.abs(self.vel[0])
        if self.pos_f[1] < 0:
            self.vel[1] = np.abs(self.vel[1])
        if self.pos_f[1] > cv.HEIGHT:
            self.vel[1] = -np.abs(self.vel[1])

        self.rect.center = self.pos_f.tolist()

    def collision_test(self, rb) :
        test_against = (self.radius + rb.radius) ** 2
        heading = rb.pos_f - self.pos_f
        mag = heading[0] * heading[0] + heading[1] * heading[1]
        if mag < test_against:
            return True, heading
        return False, None

    def collision_enter(self, rb):
        self.image = self.collision_image

    def solve_collision(self, rb, heading):
        if not rb in self.collisions:
            self.collisions.add(rb)
            rb.collisions.add(self)
            goal = cv.normalize(heading) * (self.radius + rb.radius)
            
            # if one object can't be pushed, only move other
            # if both objects can't be pushed, push both for now
            if self.can_be_pushed ^ rb.can_be_pushed:
                offset = (goal - heading)
                if self.can_be_pushed:
                    self.pos_f -= offset
                else:
                    rb.pos_f += offset
            else:
                # simple case, equal displacement - 
                # push both objects apart equally so they no longer touch
                offset = (goal - heading) / 2
                self.pos_f -= offset
                rb.pos_f += offset
            self.rect.center = self.pos_f.tolist()
            rb.rect.center = rb.pos_f.tolist()
        


