import pygame
from objects.physics.Physicsbody import PhysicsBody


class Drop(PhysicsBody):
    def __init__(self, x, y):
        super().__init__(x, y, width=20, height=20, use_gravity=True)

    def update(self, platforms, ground_y, dt):
        self.physics_update(dt, platforms, ground_y)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 215, 0), self.rect, border_radius=4)
