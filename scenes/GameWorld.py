import pygame

from objects.Collisions import Collisions
from objects.enemies.TowerEnemy import TowerEnemy
from objects.enemies.FlyEnemy import FlyEnemy
from scenes.GameScene import GameScene
from objects.Player import Player
from objects.enemies.Enemy import Enemy
from objects.Platform import Platform
from levels.Levels import LEVELS
from scenes.MainMenu import MainMenu


class GameWorld(GameScene):

    def __init__(self):
        super().__init__()

        self.font = pygame.font.SysFont("Arial", 40)

        self.ground_y = 1000

        self.player_projectiles = []
        self.enemy_projectiles = []
        self.drops = []

        self.player = Player(100, self.ground_y - 50)

        self.level = 1

        self.platforms = []
        self.enemies = []

        self.setup_level(self.level)

    def setup_level(self, level):

        self.platforms = []
        self.enemies = []
        self.drops = []

        if level not in LEVELS:
            print("Fim do jogo")
            return

        for data in LEVELS[level]:
            self.platforms.append(Platform(*data))

        if level == 0:

            self.enemies.append(Enemy(500, 800))
            self.enemies.append(Enemy(600, 800))

            self.enemies.append(TowerEnemy(1600, 500))
            self.enemies.append(TowerEnemy(1600, 1200))

            self.enemies.append(FlyEnemy(200, 100))
            self.enemies.append(FlyEnemy(1500, 300, speed=-1.2))

    def update(self):

        keys = pygame.key.get_pressed()

        self.handle_player_input(keys)

        self.update_platforms()
        self.update_player()
        self.update_enemies()

        self.update_projectiles()
        self.update_drops()

        self.check_collisions()

        self.handle_level_transitions()

    def handle_player_input(self, keys):

        self.player.handle_input(keys)

        if keys[pygame.K_SPACE]:
            self.player.shoot(self.player_projectiles)

    def update_platforms(self):

        for plat in self.platforms:
            plat.update()

    def update_player(self):

        ground_y = self.ground_y if self.level == 0 else None

        self.player.update(self.platforms, ground_y)

        screen_width = pygame.display.get_surface().get_width()

        self.player.x = max(
            0,
            min(self.player.x, screen_width - self.player.width)
        )

    def update_enemies(self):

        for enemy in self.enemies:
            enemy.update(
                self.platforms,
                self.ground_y,
                self.enemy_projectiles
            )

    def update_projectiles(self):

        screen_width = pygame.display.get_surface().get_width()

        for proj in self.enemy_projectiles[:]:

            proj.update()

            if proj.x < 0 or proj.x > screen_width:
                self.enemy_projectiles.remove(proj)

        for proj in self.player_projectiles[:]:
            proj.update()

    def update_drops(self):

        ground_y = self.ground_y if self.level == 0 else None

        for drop in self.drops[:]:
            drop.update(self.platforms, ground_y)

    def check_collisions(self):

        if Collisions.check_enemy_projectile_player(self):
            return

        if Collisions.check_player_enemy(self):
            return

        Collisions.check_player_projectiles(self)
        Collisions.check_projectile_platforms(self)
        Collisions.check_player_drops(self)
        Collisions.remove_dead_enemies(self)

    def handle_level_transitions(self):

        if self.player.y < 0:
            self.level += 1
            self.setup_level(self.level)
            self.player.y = self.ground_y - self.player.height

        elif self.player.y > self.ground_y and self.level > 0:
            self.level -= 1
            self.setup_level(self.level)
            self.player.y = 0

        if self.level == 0 and self.player.y + self.player.height > self.ground_y:
            self.player.y = self.ground_y - self.player.height
            self.player.vel_y = 0
            self.player.jumping = False

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.next_scene = MainMenu()

    def render(self, screen):

        screen.fill((20, 120, 20))

        for plat in self.platforms:
            plat.draw(screen)

        for drop in self.drops:
            drop.draw(screen)

        self.player.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        for proj in self.player_projectiles:
            proj.draw(screen)

        for proj in self.enemy_projectiles:
            proj.draw(screen)

        text = self.font.render(
            f"Fase: {self.level}",
            True,
            (255, 255, 255)
        )

        screen.blit(text, (350, 50))
