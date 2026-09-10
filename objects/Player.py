import pygame
from objects.physics.Battleentity import BattleEntity
from objects.physics.Vector2 import Vector2
from objects.graphics.AnimationSet import AnimationSet
from objects.Projectile import Projectile

WALK_SPEED = 300
JUMP_SPEED = -720


class Player(BattleEntity):
    def __init__(self, x, y, audio, width=50, height=50):
        super().__init__(x, y, width, height, hp=5)

        self.audio = audio
        self.walk_speed = WALK_SPEED
        self.jump_speed = JUMP_SPEED
        self.direction = Vector2(1, 0)
        self.shoot_delay = 500

        self.animations = AnimationSet()
        self.animations.add_animation(
            "idle", "sprites/personagem.png", self.width, self.height
        )

        self.projectile_image = "sprites/tiro.png"

    def handle_input(self, keys):
        self.vel.x = 0

        if keys[pygame.K_a]:
            self.vel.x = -self.walk_speed
            self.direction = Vector2(-1, 0)

        if keys[pygame.K_d]:
            self.vel.x = self.walk_speed
            self.direction = Vector2(1, 0)

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
                    direction=self.direction,
                    image_path=self.projectile_image
                )
            )

            if self.audio:
                self.audio.play_player_shoot()

    def draw(self, screen):
        flipped = self.direction.x < 0
        image = self.animations.get_image(flipped)
        screen.blit(image, (self.pos.x, self.pos.y))
