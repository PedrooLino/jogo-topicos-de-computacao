import pygame
from objects.physics.Physicsbody import PhysicsBody


class Drop(PhysicsBody):
    def __init__(self, x, y):
        super().__init__(x, y, width=20, height=20, use_gravity=True)

        self.image = pygame.image.load("sprites/drop.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

    def update(self, platforms, ground_y, dt):
        self.physics_update(dt, platforms, ground_y)

    def draw(self, screen):
        screen.blit(self.image, (self.pos.x, self.pos.y))
