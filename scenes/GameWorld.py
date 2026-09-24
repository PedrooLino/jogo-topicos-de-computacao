import pygame
from objects.enemies.TowerEnemy import TowerEnemy
from objects.enemies.FlyEnemy import FlyEnemy
from objects.enemies.Boss import Boss
from scenes.GameScene import GameScene
from objects.Player import Player
from objects.enemies.Enemy import Enemy
from objects.Platform import Platform
from levels.Levels import LEVELS
from scenes.DeathMenu import DeathMenu
from scenes.PauseMenu import PauseMenu
from scenes.VictoryMenu import VictoryMenu


class GameWorld(GameScene):

    def __init__(self, audio, scene_manager):
        super().__init__()

        self.audio = audio
        self.scene_manager = scene_manager

        self.audio.play_background_music()
        self.font = pygame.font.SysFont("Arial", 40)
        self.ground_y = 1000

        self.player_projectiles = []
        self.enemy_projectiles = []
        self.drops = []

        self.player = Player(100, self.ground_y - 50, self.audio)
        self.score = 0
        self.level = 2
        self.platforms = []
        self.enemies = []


        self.background = pygame.image.load("sprites/fundo.jpg").convert()

        self.background = pygame.transform.scale(
            self.background,
            pygame.display.get_surface().get_size()
        )


        self.dt = 0.0
        self._last_time = pygame.time.get_ticks()

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
            self.enemies.append(Enemy(500, 800, audio=self.audio))
            self.enemies.append(Enemy(600, 800, audio=self.audio))
            self.enemies.append(TowerEnemy(1600, 500, audio=self.audio))
            self.enemies.append(TowerEnemy(1600, 1200, audio=self.audio))
            self.enemies.append(FlyEnemy(200, 100, audio=self.audio))
            self.enemies.append(FlyEnemy(1500, 300, speed=-72, audio=self.audio))
        
        if level == 1:
            self.enemies.append(FlyEnemy(200, 100, audio=self.audio))
            self.enemies.append(FlyEnemy(1500, 300, speed=-72, audio=self.audio))
            self.enemies.append(FlyEnemy(450, 600, speed=40, audio=self.audio))
        
        if level == 2:
            self.enemies.append(Boss(1000, 840, self.player, audio=self.audio))

    def update(self):
        now = pygame.time.get_ticks()
        self.dt = min((now - self._last_time) / 1000.0, 0.1)
        self._last_time = now

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
        self.player.update(self.platforms, ground_y, self.dt)

        screen_width = pygame.display.get_surface().get_width()
        self.player.pos.x = max(
            0, min(self.player.pos.x, screen_width - self.player.width))

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update(
                self.platforms,
                self.ground_y,
                self.enemy_projectiles,
                self.dt
            )

    def update_projectiles(self):
        screen_width = pygame.display.get_surface().get_width()
        dt = self.dt

        for proj in self.enemy_projectiles[:]:
            proj.update(dt)
            if proj.pos.x < 0 or proj.pos.x > screen_width:
                self.enemy_projectiles.remove(proj)

        for proj in self.player_projectiles[:]:
            proj.update(dt)

            hit = False

            for enemy in self.enemies:
                if proj.collides_with(enemy):
                    enemy.take_damage(1)
                    hit = True

                    if not enemy.alive:

                        #som de morte
                        self.audio.play_enemy_die()

                        #pontos
                        self.score += enemy.points

                        #drop
                        drop = enemy.try_drop()
                        if drop:
                            self.drops.append(drop)

                    break

            if hit:
                self.player_projectiles.remove(proj)
                continue

            for plat in self.platforms:
                if proj.collides_with(plat):
                    self.player_projectiles.remove(proj)
                    break

        for proj in self.enemy_projectiles[:]:
            for plat in self.platforms:
                if proj.collides_with(plat):
                    self.enemy_projectiles.remove(proj)
                    break

    def update_drops(self):
        ground_y = self.ground_y if self.level == 0 else None

        for drop in self.drops[:]:
            drop.update(self.platforms, ground_y, self.dt)

            if drop.collides_with(self.player):
                self.drops.remove(drop)


    def check_collisions(self):

        for proj in self.enemy_projectiles:
            if proj.collides_with(self.player):
                self.scene_manager.push(
                    DeathMenu(self.audio, self.scene_manager)
                )
                return

        for enemy in self.enemies:
            if self.player.collides_with(enemy):
                self.scene_manager.push(
                    DeathMenu(self.audio, self.scene_manager)
                )
                return

        if (
            self.level == 2
            and self.enemies
            and all(not enemy.alive for enemy in self.enemies)
        ):
            self.scene_manager.push(
                VictoryMenu(
                    self.audio,
                    self.scene_manager
                )
            )
            return

        self.enemies = [
            e for e in self.enemies
            if e.alive
        ]


    def handle_level_transitions(self):
        if self.player.pos.y < 0:
            self.level += 1
            self.setup_level(self.level)
            self.player.pos.y = self.ground_y - self.player.height

        elif self.player.pos.y > self.ground_y and self.level > 0:
            self.level -= 1
            self.setup_level(self.level)
            self.player.pos.y = 0

        if self.level == 0 and self.player.pos.y + self.player.height > self.ground_y:
            self.player.pos.y = self.ground_y - self.player.height
            self.player.vel.y = 0
            self.player.on_ground = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene_manager.push(
                    PauseMenu(self.audio, self.scene_manager)
                )

    def render(self, screen):

        screen.blit(self.background, (0, 0))

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

        #fase
        level_text = self.font.render(
            f"Fase: {self.level}",
            True,
            (255, 255, 255)
        )
        screen.blit(level_text, (20, 20))

        #ponyo
        score_text = self.font.render(
            f"Pontos: {self.score}",
            True,
            (139, 0, 0)
        )

        screen.blit(
            score_text,
            (
                screen.get_width() - score_text.get_width() - 20,
                20
            )
        )
