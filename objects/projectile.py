import pygame
from objects.Physicsbody import PhysicsBody
from objects.Vector2 import Vector2

PROJ_SPEED = 420  # px/s


class Projectile(PhysicsBody):
    def __init__(self, x, y, direction=1, dir_y=0):
        super().__init__(x, y, width=10, height=10, use_gravity=False)

        self.vel = Vector2(PROJ_SPEED * direction, PROJ_SPEED * dir_y)
        self.color = (255, 255, 0)

    def update(self, dt, *args):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.pos.x + self.width // 2),
             int(self.pos.y + self.height // 2)),
            5
        )
