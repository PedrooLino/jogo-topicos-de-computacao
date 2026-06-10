import pygame
from objects.physics.Battleentity import BattleEntity  # type: ignore
from objects.Projectile import Projectile

WALK_SPEED = 300
JUMP_SPEED = -720


class Player(BattleEntity):
    def __init__(self, x, y, width=50, height=50):
        super().__init__(x, y, width, height, hp=5)

        self.walk_speed = WALK_SPEED
        self.jump_speed = JUMP_SPEED
        self.direction = 1
        self.shoot_delay = 500

        self.image = pygame.image.load("sprites/personagem.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image_left = pygame.transform.flip(self.image, True, False)

        self.projectile_image = "sprites/tiro.png"

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
                    self.direction,
                    image_path=self.projectile_image
                )
            )

    def draw(self, screen):

        if self.direction == 1:
            screen.blit(self.image, (self.pos.x, self.pos.y))
        else:
            screen.blit(self.image_left, (self.pos.x, self.pos.y))
