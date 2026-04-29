import pygame
from objects.GameObject import GameObject


class Projectile(GameObject):
    def __init__(self, x, y, direction=1, dir_y=0):
        super().__init__(x, y)

        self.width = 10
        self.height = 10

        self.speed_x = 7 * direction
        self.speed_y = 7 * dir_y

        self.color = (255, 255, 0)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            5
        )

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)