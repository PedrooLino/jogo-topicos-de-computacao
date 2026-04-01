import pygame
from scenes.GameScene import GameScene
from objects.player import Player
from objects.enemy import Enemy
from objects.platform import Platform
from levels.levels import LEVELS
class GameWorld(GameScene):

    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 40)
        self.ground_y = 600

        self.player_projectiles = []
        self.enemy_projectiles = []

        self.player = Player(100, self.ground_y - 50)
        self.enemies = [Enemy(400, self.ground_y - 50)]

        self.level = 0
        self.platforms = []

    def setup_level(self, level):
        self.platforms = []

        if level not in LEVELS:
            print("Fim do jogo")
            return

        for data in LEVELS[level]:
            self.platforms.append(Platform(*data))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from scenes.main_menu import MainMenu
                self.next_scene = MainMenu()

    def update(self):
        # atualizar plataformas
        for plat in self.platforms:
            plat.update()

        # input
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

        # update do player
        if self.level == 0:
            self.player.update(self.platforms, self.ground_y)
        else:
            self.player.update(self.platforms, ground_y=None)

        if not self.platforms:
            self.setup_level(self.level)

        # limitar na tela
        screen_width = pygame.display.get_surface().get_width()
        self.player.x = max(0, min(self.player.x, screen_width - self.player.width))

        # chão só na fase 0
        if self.level == 0 and self.player.y + self.player.height > self.ground_y:
            self.player.y = self.ground_y - self.player.height
            self.player.vel_y = 0
            self.player.jumping = False

        # subir de fase
        if self.player.y < 0:
            self.level += 1
            self.setup_level(self.level)
            self.player.y = self.ground_y - self.player.height

        # descer de fase
        elif self.player.y > self.ground_y and self.level > 0:
            self.level -= 1
            self.setup_level(self.level)
            self.player.y = 0

        # tiro do player
        if keys[pygame.K_SPACE]:
            self.player.shoot(self.player_projectiles)

        # inimigos
        for enemy in self.enemies:
            enemy.update(self.platforms, self.ground_y, self.enemy_projectiles)

        # tiros inimigos
        for proj in self.enemy_projectiles[:]:
            proj.update()
            if proj.x < 0 or proj.x > 1080:
                self.enemy_projectiles.remove(proj)

        # tiros do player
        for proj in self.player_projectiles[:]:
            proj.update()

            for enemy in self.enemies[:]:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if proj.get_rect().colliderect(enemy_rect):
                    self.enemies.remove(enemy)
                    self.player_projectiles.remove(proj)
                    break

        # colisões
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)

        # tiros acertando player
        for proj in self.enemy_projectiles[:]:
            if proj.get_rect().colliderect(player_rect):
                from scenes.death_menu import DeathMenu
                self.next_scene = DeathMenu()
                return

        # inimigo encostando no player
        for enemy in self.enemies:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if player_rect.colliderect(enemy_rect):
                from scenes.death_menu import DeathMenu
                self.next_scene = DeathMenu()
                return

    def render(self, screen):
        screen.fill((20, 120, 20))

        for plat in self.platforms:
            plat.draw(screen)

        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)

        for proj in self.player_projectiles:
            proj.draw(screen)

        for proj in self.enemy_projectiles:
            proj.draw(screen)
        #texto na hud só pra teste
        text = self.font.render(f"Fase: {self.level}", True, (255, 255, 255))
        screen.blit(text, (350, 50))
