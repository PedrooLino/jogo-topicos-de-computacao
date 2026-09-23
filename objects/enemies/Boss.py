import math
import random
import pygame

from objects.enemies.Enemy import Enemy
from objects.physics.Vector2 import Vector2
from objects.graphics.AnimationSet import AnimationSet
from objects.Projectile import Projectile


class Boss(Enemy):

    def __init__(
        self,
        x,
        y,
        player,
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
            image_path="sprites/amalgama/Amalgama.png",
            audio=audio
        )

        self.max_hp = 12
        self.hp = self.max_hp

        self.points = 100
        self.drop_chance = 1.0

        self.player = player

        self.vel.x = 0
        self.jump_speed = -500

        self.jump_cooldown = 3000
        self.last_jump = pygame.time.get_ticks()

        self.shoot_delay = 1500
        self.projectile_image = "sprites/bolafogo.png"

        self.phase = 1

        self.animations = AnimationSet()

        self.animations.add_animation(
            "idle",
            [
                "sprites/amalgama/Amalgama.png",
                "sprites/amalgama/Amalgama-2.png",
                "sprites/amalgama/Amalgama-3.png",
                "sprites/amalgama/Amalgama-4.png",
                "sprites/amalgama/Amalgama-5.png",
                "sprites/amalgama/Amalgama-6.png",
                "sprites/amalgama/Amalgama-7.png",
                "sprites/amalgama/Amalgama-8.png",
                "sprites/amalgama/Amalgama-9.png",
            ],
            self.width,
            self.height,
            frame_duration=0.10
        )

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

        self.animations.update(dt)

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
        if self.phase == 1:
            speed = 120

        elif self.phase == 2:
            speed = 170

        else:
            speed = 220

        boss_center = self.pos.x + self.width / 2
        player_center = self.player.pos.x + self.player.width / 2

        distance_x = player_center - boss_center

        dead_zone = 5

        if distance_x > dead_zone:
            self.vel.x = speed

        elif distance_x < -dead_zone:
            self.vel.x = -speed

        else:
            self.vel.x = 0

        self.physics_update(
            dt,
            platforms,
            ground_y
        )

        screen_width = pygame.display.get_surface().get_width()

        if self.pos.x + self.width >= screen_width:
            self.pos.x = screen_width - self.width
            self.vel.x = 0

        elif self.pos.x <= 0:
            self.pos.x = 0
            self.vel.x = 0

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

        boss_center = Vector2(
            cx,
            cy
        )

        to_player = player_center - boss_center

        direction = (
            to_player.normalized()
            if to_player.length() > 0
            else Vector2(1, 0)
        )

        self.create_projectile(
            projectiles_list,
            cx,
            cy,
            direction
        )

        if self.phase >= 2:

            spread_angle = math.radians(20)

            self.create_projectile(
                projectiles_list,
                cx,
                cy,
                direction.rotated(spread_angle)
            )

            self.create_projectile(
                projectiles_list,
                cx,
                cy,
                direction.rotated(-spread_angle)
            )

        if self.phase >= 3:

            directions = [
                Vector2(1, 0),
                Vector2(-1, 0),
                Vector2(0, 1),
                Vector2(0, -1),
            ]

            for dir_vec in directions:

                self.create_projectile(
                    projectiles_list,
                    cx,
                    cy,
                    dir_vec
                )

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

        screen.blit(
            image,
            (self.pos.x, self.pos.y)
        )

        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):

        bar_width = 400
        bar_height = 25

        x = (
            screen.get_width() // 2
            - bar_width // 2
        )

        y = 30

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
