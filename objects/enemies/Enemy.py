import pygame
from objects.physics.Battleentity import BattleEntity # type: ignore
from objects.Projectile import Projectile

PATROL_SPEED = 120  # px/s


class Enemy(BattleEntity):
    def __init__(self, x, y, width=50, height=50,
                 speed=PATROL_SPEED, color=(0, 0, 255)):
        super().__init__(x, y, width, height, hp=3, color=color)

        self.vel.x = speed
        self.shoot_delay = 1500
        self.drop_chance = 0.1

    def update(self, platforms, ground_y, projectiles_list, dt):
        screen_width = pygame.display.get_surface().get_width()

        # Guarda x antes de mover para detectar colisão lateral
        prev_x = self.pos.x

        self.apply_gravity(dt)

        # Move só em X e resolve colisão X
        self.pos.x += self.vel.x * dt
        self.resolve_x(platforms)

        # Se a posição em X não avançou na direção esperada, bateu numa parede
        moved = self.pos.x - prev_x
        if (self.vel.x > 0 and moved <= 0) or (self.vel.x < 0 and moved >= 0):
            self.vel.x *= -1

        # Move em Y e resolve colisão Y
        self.pos.y += self.vel.y * dt
        self.resolve_y(platforms, ground_y)

        # Inverte nas bordas da tela
        if self.pos.x + self.width >= screen_width or self.pos.x <= 0:
            self.vel.x *= -1

        # Tiro na direção do movimento
        if self.can_shoot():
            direction = 1 if self.vel.x > 0 else -1
            projectiles_list.append(
                Projectile(
                    self.pos.x + self.width // 2,
                    self.pos.y + self.height // 2,
                    direction
                )
            )

    def _skip_platform(self, plat):
        return False
