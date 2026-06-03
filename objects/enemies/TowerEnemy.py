import pygame
from objects.enemies.Enemy import Enemy
from objects.Projectile import Projectile


class TowerEnemy(Enemy):
    def __init__(self, x, y, color=(0, 255, 0)):
        super().__init__(x, y, speed=0, color=color)

        self.vel.x = 0
        self.hp = 5
        self.shoot_delay = 800
        self.drop_chance =0.6

    def update(self, platforms, ground_y, projectiles_list, dt):
        if self.can_shoot():
            cx = self.pos.x + self.width // 2
            cy = self.pos.y + self.height // 2
            projectiles_list.append(Projectile(cx, cy,  1))
            projectiles_list.append(Projectile(cx, cy, -1))

        self.physics_update(dt, platforms, ground_y)
