import pygame
from objects.physics.Vector2 import Vector2
from objects.physics import Collision


class GameObject:
    """
    Base de todo objeto do jogo.

    `rect` continua sendo o retângulo do sprite (posição + width/height),
    usado para desenho.

    `hitbox` é o retângulo usado para colisão, e pode ser diferente do
    sprite: por padrão é igual ao sprite (hitbox_offset=(0,0),
    hitbox_size=(width, height)), mas qualquer subclasse pode apertar
    a hitbox (ex: um personagem com sprite 100x100 mas hitbox real
    80x90) apenas alterando `self.hitbox_offset` / `self.hitbox_size`
    depois do super().__init__().
    """

    def __init__(self, x, y, width=50, height=50,
                 hitbox_offset=(0, 0), hitbox_size=None):
        self.pos = Vector2(x, y)
        self.width = width
        self.height = height

        self.hitbox_offset = Vector2(*hitbox_offset)
        self.hitbox_size = hitbox_size if hitbox_size is not None else (
            width, height)

    # ---------------- Compat x/y (delegam para o vetor pos) ----------------
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

    # ---------------- Retângulos ----------------
    @property
    def rect(self):
        """Retângulo do sprite, usado para desenho."""
        return pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    @property
    def hitbox(self):
        """Retângulo genérico de colisão (pode diferir do sprite)."""
        return Collision.get_hitbox(self)

    # ---------------- Colisão ----------------
    def collides_with(self, other):
        """Colisão genérica contra outro GameObject (usa hitbox de ambos)."""
        return Collision.check_collision(self, other)

    def collides_with_rect(self, rect):
        """Colisão genérica contra um pygame.Rect qualquer."""
        return Collision.check_collision_rect(self, rect)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
