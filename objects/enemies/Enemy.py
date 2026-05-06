import pygame
import random
from objects.GameObject import GameObject
from objects.Projectile import Projectile


class Enemy(GameObject):
    def __init__(self, x, y, width=50, height=50, speed=2, color=(0, 0, 255)):
        super().__init__(x, y, width, height)

        self.speed = speed
        self.vel_x = speed
        self.vel_y = 0

        self.gravity = 0.5
        self.use_gravity = True

        self.color = color

        self.hp = 3
        self.alive = True

        self.shoot_delay = 1500
        self.last_shot = pygame.time.get_ticks()

        self.drop_chance = 0.05

    def update(self, platforms, ground_y, projectiles_list):
        self.x += self.vel_x

        screen_width = pygame.display.get_surface().get_width()

        if self.x + self.width > screen_width or self.x < 0:
            self.vel_x *= -1

        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
            projectiles_list.append(
                Projectile(
                    self.x + self.width // 2,
                    self.y + self.height // 2,
                    1 if self.vel_x > 0 else -1
                )
            )
            self.last_shot = now

        self.vel_y += self.gravity
        self.y += self.vel_y

        self.on_ground = False
        rect = self.rect

        for plat in platforms:
            if rect.colliderect(plat.rect):
                if self.vel_y > 0 and rect.bottom - self.vel_y <= plat.rect.top:
                    self.y = plat.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                else:
                    self.vel_x *= -1
                    self.x += self.vel_x * 2
                rect = self.rect

        if ground_y is not None and self.y + self.height >= ground_y:
            self.y = ground_y - self.height
            self.vel_y = 0
            self.on_ground = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def take_damage(self, damage=1):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

    def try_drop(self):
        if random.random() < self.drop_chance:
            from objects.Drop import Drop
            return Drop(self.x + self.width // 2, self.y)
        return None