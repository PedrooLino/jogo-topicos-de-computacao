import pygame
from objects.Projectile import Projectile
from objects.enemies.Enemy import Enemy


class TowerEnemy(Enemy):
    def __init__(self, x, y, color=(0, 255, 0)):
        super().__init__(x, y, speed=0, color=color)

        self.hp = 5
        self.shoot_delay = 800

    def update(self, platforms, ground_y, projectiles_list):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            projectiles_list.append(
                Projectile(self.x + self.width // 2, self.y + self.height // 2, 1)
            )
            projectiles_list.append(
                Projectile(self.x + self.width // 2, self.y + self.height // 2, -1)
            )

            self.last_shot = now

        self.vel_y += self.gravity
        self.y += self.vel_y

        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for plat in platforms:
            if enemy_rect.colliderect(plat.rect):
                if self.vel_y > 0 and enemy_rect.bottom - self.vel_y <= plat.rect.top:
                    self.y = plat.rect.top - self.height
                    self.vel_y = 0
                    self.jumping = False

        if self.y + self.height >= ground_y:
            self.y = ground_y - self.height
            self.vel_y = 0
            self.jumping = False