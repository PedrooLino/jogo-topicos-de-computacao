import pygame
import math
from objects.enemies.Enemy import Enemy
from objects.physics.Vector2 import Vector2
from objects.Projectile import Projectile

FLY_SPEED = 72


class FlyEnemy(Enemy):
    def __init__(self, x, y,
                 speed=FLY_SPEED,
                 amplitude=50,
                 image_path="sprites/DemonioVoador.png", audio=None):

        # Corrigido: antes image_path e audio não eram repassados ao
        # Enemy, então o FlyEnemy sempre nascia com self.audio=None
        # (nunca tocava som de tiro) e recarregava a imagem "na mão"
        # logo em seguida.
        super().__init__(x, y, speed=speed, color=(128, 0, 128),
                         image_path=image_path, audio=audio)

        self.points = 15
        self.base_y = float(y)
        self.amplitude = amplitude
        self.time = 0.0

        self.hp = 2
        self.shoot_delay = 1800
        self.drop_chance = 0.5
        self.use_gravity = False

        self.projectile_image = "sprites/bolafogo.png"

    def update(self, platforms, ground_y, projectiles_list, dt):
        screen_width = pygame.display.get_surface().get_width()

        self.pos.x += self.vel.x * dt

        if self.pos.x + self.width >= screen_width or self.pos.x <= 0:
            self.vel.x *= -1

        self.time += dt
        self.pos.y = self.base_y + self.amplitude * \
            math.sin(self.time * math.pi)

        if self.can_shoot():
            projectiles_list.append(
                Projectile(
                    self.pos.x + self.width // 2,
                    self.pos.y + self.height,
                    direction=Vector2(0, 1),
                    image_path=self.projectile_image
                )
            )
            if self.audio:
                self.audio.play_enemy_shoot()

    def draw(self, screen):
        # Sprite base do FlyEnemy olha para a esquerda, por isso a
        # lógica de espelhamento é invertida em relação ao Enemy comum.
        flipped = self.vel.x > 0
        image = self.animations.get_image(flipped)
        screen.blit(image, (self.pos.x, self.pos.y))
