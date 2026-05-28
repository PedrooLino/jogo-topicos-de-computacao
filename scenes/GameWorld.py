import pygame
from objects.enemies.TowerEnemy import TowerEnemy
from objects.enemies.FlyEnemy import FlyEnemy
from scenes.GameScene import GameScene
from objects.Player import Player
from objects.enemies.Enemy import Enemy
from objects.Platform import Platform
from levels.Levels import LEVELS
from scenes.DeathMenu import DeathMenu
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

        # dt em segundos — calculado a cada frame
        self.dt = 0.0
        self._last_time = pygame.time.get_ticks()

        self.setup_level(self.level)

    # ------------------------------------------------------------------ #
    #  Setup                                                               #
    # ------------------------------------------------------------------ #

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
            self.enemies.append(FlyEnemy(1500, 300, speed=-72))

    # ------------------------------------------------------------------ #
    #  Loop principal                                                      #
    # ------------------------------------------------------------------ #

    def update(self):
        # Calcula dt em segundos com cap de 100ms (evita saltos ao travar)
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

    # ------------------------------------------------------------------ #
    #  Sub-updates                                                         #
    # ------------------------------------------------------------------ #

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
        self.player.x = max(
            0, min(self.player.x, screen_width - self.player.width))

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update(self.platforms, self.ground_y,
                         self.enemy_projectiles, self.dt)

    def update_projectiles(self):
        screen_width = pygame.display.get_surface().get_width()
        dt = self.dt

        # Projéteis inimigos — mover e remover fora da tela
        for proj in self.enemy_projectiles[:]:
            proj.update(dt)
            if proj.x < 0 or proj.x > screen_width:
                self.enemy_projectiles.remove(proj)

        # Projéteis do player — mover, checar hit em inimigos
        for proj in self.player_projectiles[:]:
            proj.update(dt)

            hit = False
            for enemy in self.enemies:
                if proj.rect.colliderect(enemy.rect):
                    enemy.take_damage(1)
                    hit = True

                    if not enemy.alive:
                        drop = enemy.try_drop()
                        if drop:
                            self.drops.append(drop)
                    break

            if hit and proj in self.player_projectiles:
                self.player_projectiles.remove(proj)
                continue

            # Colisão com plataformas
            for plat in self.platforms:
                if proj.rect.colliderect(plat.rect):
                    if proj in self.player_projectiles:
                        self.player_projectiles.remove(proj)
                    break

        # Projéteis inimigos — colisão com plataformas
        for proj in self.enemy_projectiles[:]:
            for plat in self.platforms:
                if proj.rect.colliderect(plat.rect):
                    if proj in self.enemy_projectiles:
                        self.enemy_projectiles.remove(proj)
                    break

    def update_drops(self):
        ground_y = self.ground_y if self.level == 0 else None

        for drop in self.drops[:]:
            drop.update(self.platforms, ground_y, self.dt)

            if drop.rect.colliderect(self.player.rect):
                self.drops.remove(drop)
                # efeito do drop será definido depois

    # ------------------------------------------------------------------ #
    #  Colisões e transições                                               #
    # ------------------------------------------------------------------ #

    def check_collisions(self):
        player_rect = self.player.rect

        for proj in self.enemy_projectiles:
            if proj.rect.colliderect(player_rect):
                self.next_scene = DeathMenu()
                return

        for enemy in self.enemies:
            if player_rect.colliderect(enemy.rect):
                self.next_scene = DeathMenu()
                return

        self.enemies = [e for e in self.enemies if e.alive]

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
            self.player.on_ground = True

    # ------------------------------------------------------------------ #
    #  Eventos e render                                                    #
    # ------------------------------------------------------------------ #

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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

        text = self.font.render(f"Fase: {self.level}", True, (255, 255, 255))
        screen.blit(text, (350, 50))
