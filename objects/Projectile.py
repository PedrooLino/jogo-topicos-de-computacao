import pygame
from objects.physics.Physicsbody import PhysicsBody
from objects.physics.Vector2 import Vector2

PROJ_SPEED = 420


class Projectile(PhysicsBody):
    def __init__(self, x, y, direction=1, dir_y=0, image_path="sprites/tiro.png"):
        super().__init__(x, y, width=10, height=10, use_gravity=False)

        self.vel = Vector2(
            PROJ_SPEED * direction,
            PROJ_SPEED * dir_y
        )

        self.direction = direction

        # imagem dinâmica
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

        self.image_left = pygame.transform.flip(self.image, True, False)

    def update(self, dt, *args):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

    def draw(self, screen):

        img = self.image if self.vel.x >= 0 else self.image_left

        screen.blit(img, (self.pos.x, self.pos.y))
