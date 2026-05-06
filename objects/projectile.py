import pygame
from objects.GameObject import GameObject


class Projectile(GameObject):
    def __init__(self, x, y, direction=1, dir_y=0):
        super().__init__(x, y, 10, 10)

        self.vel_x = 7 * direction
        self.vel_y = 7 * dir_y
        self.color = (255, 255, 0)

    def update(self, *args):
        self.move()

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            5
        )