import pygame
import math
from objects.enemies.Enemy import Enemy
from objects.Projectile import Projectile
 
 
class FlyEnemy(Enemy):
    def __init__(self, x, y, speed=1.2, amplitude=50):
        super().__init__(x, y, speed=speed, color=(128, 0, 128))
 
        self.base_y = y
        self.amplitude = amplitude
        self.time = 0
 
        self.hp = 2
        self.shoot_delay = 1800
 
        # Chance de drop ao morrer (10%)
        self.drop_chance = 0.10
 
    def update(self, platforms, ground_y, projectiles_list):
        self.x += self.speed
        screen_width = pygame.display.get_surface().get_width()
 
        if self.x + self.width > screen_width or self.x < 0:
            self.speed *= -1
 
        self.time += 0.03
        self.y = self.base_y + self.amplitude * math.sin(self.time)
 
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            projectiles_list.append(
                Projectile(
                    self.x + self.width // 2,
                    self.y + self.height,
                    0,
                    1
                )
            )
            self.last_shot = now