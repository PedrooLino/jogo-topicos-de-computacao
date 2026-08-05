import pygame
from objects.enemies.Enemy import Enemy
from objects.Projectile import Projectile


class TowerEnemy(Enemy):
    def __init__(self, x, y,
                 image_path="sprites/DemonioTorre.png",
                 color=(0, 255, 0)):

        super().__init__(x, y, speed=0, color=color)

        self.points = 30
        self.vel.x = 0
        self.hp = 5
        self.shoot_delay = 800
        self.drop_chance = 0.6

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

        self.projectile_image = "sprites/bolafogo.png"

    def update(self, platforms, ground_y, projectiles_list, dt):

        if self.can_shoot():

            cx = self.pos.x + self.width // 2
            cy = self.pos.y + self.height // 2

            projectiles_list.append(
                Projectile(
                    cx,
                    cy,
                    1,
                    image_path=self.projectile_image
                )
            )

            projectiles_list.append(
                Projectile(
                    cx,
                    cy,
                    -1,
                    image_path=self.projectile_image
                )
            )

        self.physics_update(dt, platforms, ground_y)

    def draw(self, screen):
        screen.blit(self.image, (self.pos.x, self.pos.y))
