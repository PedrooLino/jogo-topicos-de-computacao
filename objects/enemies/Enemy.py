import pygame
from objects.Battleentity import BattleEntity # type: ignore
from objects.Projectile import Projectile

PATROL_SPEED = 120  # px/s


class Enemy(BattleEntity):
    def __init__(self, x, y, width=50, height=50,
                 speed=PATROL_SPEED, color=(0, 0, 255)):
        super().__init__(x, y, width, height, hp=3, color=color)

        self.vel.x = speed
        self.shoot_delay = 1500
        self.drop_chance = 0.01

    def update(self, platforms, ground_y, projectiles_list, dt):
        screen_width = pygame.display.get_surface().get_width()

        if self.pos.x + self.width >= screen_width or self.pos.x <= 0:
            self.vel.x *= -1

        if self.can_shoot():
            direction = 1 if self.vel.x > 0 else -1
            projectiles_list.append(
                Projectile(
                    self.pos.x + self.width // 2,
                    self.pos.y + self.height // 2,
                    direction
                )
            )

        self.physics_update(dt, platforms, ground_y)

        # Inversão ao colidir lateralmente com plataforma
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                self.vel.x *= -1
                self.pos.x += self.vel.x * dt * 2
                break

    def _skip_platform(self, plat):
        return False
