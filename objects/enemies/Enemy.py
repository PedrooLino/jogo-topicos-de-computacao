import pygame
from objects.physics.Battleentity import BattleEntity
from objects.physics.Vector2 import Vector2
from objects.graphics.AnimationSet import AnimationSet
from objects.Projectile import Projectile

PATROL_SPEED = 120


class Enemy(BattleEntity):
    def __init__(self, x, y, width=50, height=50,
                 speed=PATROL_SPEED, color=(0, 0, 255),
                 image_path="sprites/Demonio.png", audio=None):

        super().__init__(x, y, width, height, hp=3, color=color)

        self.audio = audio
        self.points = 10
        self.vel.x = speed
        self.shoot_delay = 1500
        self.drop_chance = 0.1

        self.animations = AnimationSet()
        self.animations.add_animation(
            "idle", image_path, self.width, self.height)

        self.projectile_image = "sprites/bolafogo.png"

    def update(self, platforms, ground_y, projectiles_list, dt):
        screen_width = pygame.display.get_surface().get_width()

        prev_x = self.pos.x

        self.apply_gravity(dt)

        self.pos.x += self.vel.x * dt
        self.resolve_x(platforms)

        moved = self.pos.x - prev_x

        if (self.vel.x > 0 and moved <= 0) or (self.vel.x < 0 and moved >= 0):
            self.vel.x *= -1

        self.pos.y += self.vel.y * dt
        self.resolve_y(platforms, ground_y)

        if self.pos.x + self.width >= screen_width or self.pos.x <= 0:
            self.vel.x *= -1

        if self.can_shoot():
            direction = Vector2(1 if self.vel.x > 0 else -1, 0)

            projectiles_list.append(
                Projectile(
                    self.pos.x + self.width // 2,
                    self.pos.y + self.height // 2,
                    direction=direction,
                    image_path=self.projectile_image
                )
            )
            if self.audio:
                self.audio.play_enemy_shoot()

    def draw(self, screen):
        flipped = self.vel.x <= 0
        image = self.animations.get_image(flipped)
        screen.blit(image, (self.pos.x, self.pos.y))

    def _skip_platform(self, plat):
        return False
