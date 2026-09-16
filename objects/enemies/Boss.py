import math
import random
import pygame

from objects.enemies.Enemy import Enemy
from objects.physics.Vector2 import Vector2
from objects.Projectile import Projectile


class Boss(Enemy):

    def __init__(
        self,
        x,
        y,
        player,
        image_path="sprites/Amalgama.png",
        color=(150, 0, 0),
        audio=None
    ):
        super().__init__(
            x,
            y,
            width=100,
            height=100,
            speed=120,
            color=color,
            image_path=image_path,
            audio=audio
        )
        # Enemy.__init__ já carrega a imagem em self.animations,
        # então não é necessário recarregar/reescalar de novo aqui.

        self.max_hp = 10
        self.hp = self.max_hp

        self.points = 1000
        self.drop_chance = 1.0

        self.player = player

        self.vel.x = 120

        self.jump_speed = -500
        self.jump_cooldown = 3000
        self.last_jump = pygame.time.get_ticks()

        self.shoot_delay = 1500
        self.projectile_image = "sprites/bolafogo.png"

        self.phase = 1

    def update(
        self,
        platforms,
        ground_y,
        projectiles_list,
        dt
    ):
        if not self.alive:
            return

        self.update_phase()

        self.update_movement(
            platforms,
            ground_y,
            dt
        )

        self.update_attack(
            projectiles_list
        )

    def update_phase(self):

        hp_percent = self.hp / self.max_hp

        if hp_percent > 0.66:
            self.phase = 1

        elif hp_percent > 0.33:
            self.phase = 2

        else:
            self.phase = 3

    def update_movement(
        self,
        platforms,
        ground_y,
        dt
    ):
        previous_x = self.pos.x

        # Física normal do jogo
        self.physics_update(
            dt,
            platforms,
            ground_y
        )

        moved = self.pos.x - previous_x

        # bateu horizontalmente em alguma plataforma
        if (
            (self.vel.x > 0 and moved <= 0)
            or
            (self.vel.x < 0 and moved >= 0)
        ):
            self.vel.x *= -1

        # velocidade depende da fase
        if self.phase == 1:
            speed = 120

        elif self.phase == 2:
            speed = 170

        else:
            speed = 220

        if self.vel.x > 0:
            self.vel.x = speed
        else:
            self.vel.x = -speed

        # limites da tela
        screen_width = pygame.display.get_surface().get_width()

        if self.pos.x + self.width >= screen_width:
            self.pos.x = screen_width - self.width
            self.vel.x = -abs(self.vel.x)

        elif self.pos.x <= 0:
            self.pos.x = 0
            self.vel.x = abs(self.vel.x)

        # Pulo
        self.try_jump()

    def try_jump(self):

        now = pygame.time.get_ticks()

        if now - self.last_jump < self.jump_cooldown:
            return

        if not self.on_ground:
            return

        if self.phase == 1:
            chance = 0.01

        elif self.phase == 2:
            chance = 0.025

        else:
            chance = 0.05

        if random.random() < chance:

            self.vel.y = self.jump_speed
            self.on_ground = False

            self.last_jump = now

    def update_attack(self, projectiles_list):

        if self.phase == 1:
            self.shoot_delay = 1500

        elif self.phase == 2:
            self.shoot_delay = 1000

        else:
            self.shoot_delay = 650

        if self.can_shoot():
            self.shoot(projectiles_list)

    def shoot(self, projectiles_list):

        cx = self.pos.x + self.width / 2
        cy = self.pos.y + self.height / 2

        player_center = Vector2(
            self.player.pos.x + self.player.width / 2,
            self.player.pos.y + self.player.height / 2
        )

        to_player = player_center - Vector2(cx, cy)
        direction = (
            to_player.normalized()
            if to_player.length() > 0
            else Vector2(1, 0)
        )

        self.create_projectile(projectiles_list, cx, cy, direction)

        if self.phase >= 2:
            spread_angle = math.radians(20)

            self.create_projectile(
                projectiles_list, cx, cy, direction.rotated(spread_angle)
            )
            self.create_projectile(
                projectiles_list, cx, cy, direction.rotated(-spread_angle)
            )

        if self.phase >= 3:
            directions = [
                Vector2(1, 0),
                Vector2(-1, 0),
                Vector2(0, 1),
                Vector2(0, -1),
            ]

            for dir_vec in directions:
                self.create_projectile(projectiles_list, cx, cy, dir_vec)

        if self.audio:
            self.audio.play_enemy_shoot()

    def create_projectile(
        self,
        projectiles_list,
        x,
        y,
        direction
    ):

        projectile = Projectile(
            x,
            y,
            direction=direction,
            image_path=self.projectile_image
        )

        projectiles_list.append(projectile)

    def draw(self, screen):

        flipped = self.vel.x < 0
        image = self.animations.get_image(flipped)
        screen.blit(image, (self.pos.x, self.pos.y))

        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):

        bar_width = 400
        bar_height = 25

        x = (
            screen.get_width() // 2
            - bar_width // 2
        )

        y = 30

        # fundo
        pygame.draw.rect(
            screen,
            (60, 60, 60),
            (
                x,
                y,
                bar_width,
                bar_height
            )
        )

        # vida
        hp_width = int(
            bar_width *
            (self.hp / self.max_hp)
        )

        if self.phase == 1:
            color = (0, 200, 0)

        elif self.phase == 2:
            color = (255, 180, 0)

        else:
            color = (255, 0, 0)

        pygame.draw.rect(
            screen,
            color,
            (
                x,
                y,
                hp_width,
                bar_height
            )
        )

        # borda
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                x,
                y,
                bar_width,
                bar_height
            ),
            2
        )

        # texto
        font = pygame.font.SysFont(
            "Arial",
            25,
            bold=True
        )

        text = font.render(
            "Amalgama",
            True,
            (255, 255, 255)
        )

        screen.blit(
            text,
            (
                screen.get_width() // 2
                - text.get_width() // 2,
                y - 30
            )
        )
