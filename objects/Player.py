import pygame
from objects.physics.Battleentity import BattleEntity # type: ignore
from objects.Projectile import Projectile

WALK_SPEED = 300    # px/s
JUMP_SPEED = -720   # px/s


class Player(BattleEntity):
    def __init__(self, x, y, width=50, height=50):
        super().__init__(x, y, width, height, hp=5, color=(255, 0, 0))

        self.walk_speed = WALK_SPEED
        self.jump_speed = JUMP_SPEED
        self.direction = 1
        self.shoot_delay = 500

    def handle_input(self, keys):
        self.vel.x = 0

        if keys[pygame.K_a]:
            self.vel.x = -self.walk_speed
            self.direction = -1

        if keys[pygame.K_d]:
            self.vel.x = self.walk_speed
            self.direction = 1

        if keys[pygame.K_w] and self.on_ground:
            self.vel.y = self.jump_speed
            self.on_ground = False

    def update(self, platforms, ground_y, dt):
        self.physics_update(dt, platforms, ground_y)

    def _on_land(self, plat):
        if hasattr(plat, "trigger"):
            plat.trigger()

    def shoot(self, projectiles_list):
        if self.can_shoot():
            projectiles_list.append(
                Projectile(
                    self.pos.x + self.width // 2,
                    self.pos.y + self.height // 2,
                    self.direction
                )
            )
