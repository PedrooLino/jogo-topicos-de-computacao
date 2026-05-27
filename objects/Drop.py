import pygame
from objects.GameObject import GameObject


class Drop(GameObject):

    def __init__(self, x, y):

        super().__init__(x, y, 20, 20)

        self.gravity = 0.4

        self.use_gravity = True

    def update(self, platforms, ground_y):

        self.apply_gravity()

        self.move()

        self.collide_y(platforms)

        if ground_y is not None and self.y + self.height >= ground_y:

            self.y = ground_y - self.height

            self.vel_y = 0

            self.on_ground = True

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            (255, 215, 0),
            self.rect,
            border_radius=4
        )
