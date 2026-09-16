import pygame
from objects.physics.Vector2 import Vector2
from objects.physics import Collision


class GameObject:

    def __init__(self, x, y, width=50, height=50,
                 hitbox_offset=(0, 0), hitbox_size=None):
        self.pos = Vector2(x, y)
        self.width = width
        self.height = height

        self.hitbox_offset = Vector2(*hitbox_offset)
        self.hitbox_size = hitbox_size if hitbox_size is not None else (
            width, height)

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
        """Retângulo do sprite, usado para desenho."""
        return pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    @property
    def hitbox(self):
        """Retângulo genérico de colisão (pode diferir do sprite)."""
        return Collision.get_hitbox(self)


    def collides_with(self, other):
        """Colisão genérica contra outro GameObject (usa hitbox de ambos)."""
        return Collision.check_collision(self, other)

    def collides_with_rect(self, rect):
        """Colisão genérica contra um pygame.Rect qualquer."""
        return Collision.check_collision_rect(self, rect)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
