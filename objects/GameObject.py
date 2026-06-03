import pygame
from objects.physics.Vector2 import Vector2


class GameObject:
    def __init__(self, x, y, width=50, height=50):
        self.pos = Vector2(x, y)
        self.width = width
        self.height = height

    @property
    def x(self):
        return self.pos.x

    @x.setter
    def x(self, value):
        self.pos.x = float(value)

    @property
    def y(self):
        return self.pos.y

    @y.setter
    def y(self, value):
        self.pos.y = float(value)

    @property
    def rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
