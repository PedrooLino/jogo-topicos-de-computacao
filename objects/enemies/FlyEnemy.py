import pygame
import math
from objects.enemies.Enemy import Enemy
from objects.Projectile import Projectile

FLY_SPEED = 72 


class FlyEnemy(Enemy):
    def __init__(self, x, y,
                 speed=FLY_SPEED,
                 amplitude=50,
                 image_path="sprites/DemonioVoador.png"):

        super().__init__(x, y, speed=speed, color=(128, 0, 128))

        self.base_y = float(y)
        self.amplitude = amplitude
        self.time = 0.0

        self.hp = 2
        self.shoot_delay = 1800
        self.drop_chance = 0.5
        self.use_gravity = False

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

    def update(self, platforms, ground_y, projectiles_list, dt):
        screen_width = pygame.display.get_surface().get_width()

        self.pos.x += self.vel.x * dt

        if self.pos.x + self.width >= screen_width or self.pos.x <= 0:
            self.vel.x *= -1

        self.time += dt
        self.pos.y = self.base_y + self.amplitude * \
            math.sin(self.time * math.pi)

        if self.can_shoot():
            projectiles_list.append(
                Projectile(
                    self.pos.x + self.width // 2,
                    self.pos.y + self.height,
                    0, 1
                )
            )

    def draw(self, screen):
        screen.blit(self.image, (self.pos.x, self.pos.y))
