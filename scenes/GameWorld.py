import pygame
from scenes.GameScene import GameScene
from objects.player import Player
from objects.enemy import Enemy
from objects.platform import Platform

class GameWorld(GameScene):

    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 40)
        self.ground_y = 600  # altura base da fase

        # jogador e inimigos
        self.player = Player(100, self.ground_y - 50)
        self.enemies = [Enemy(400, self.ground_y - 50)]

        # fase inicial
        self.level = 1
        self.platforms = []

    def setup_level(self, level):
        #plataformas da fase
        #x, y, largura, altura
        if level == 0:
            self.platforms = [
                Platform(240, 50, 100, 10, "esse é o pul final"),
                Platform(120, 130, 100, 10, "pulo final"),
                Platform(180, 220, 200, 10, "pré pulo final"),
                Platform(560, 280, 200, 10, "depois do toco"),
                Platform(500, 370, 20, 10, "toquim"),
                Platform(370, 450, 50, 10, "meio"),
                Platform(120, 500, 100, 10, "moeda"),
                Platform(560, 520, 200, 10, "primeira")
            ]
        elif level == 1:
            self.platforms = [
                Platform(200, 520, 150, 10, "primeira"),
                Platform(450, 430, 150, 10, "segunda"),
                Platform(300, 340, 150, 10, "terceiro"),
                Platform(100, 250, 150, 10, "quarta"),
                Platform(400, 160, 150, 10, "quinta"),
                Platform(600, 70, 150, 10, "sexta")
            ]
        elif level == 2:
            self.platforms = [
                Platform(300, 600, 150, 10, "primeira"),
                Platform(450, 510, 150, 10, "segunda"),
                Platform(300, 420, 150, 10, "terceiro"),
                Platform(100, 330, 150, 10, "quarta"),
                Platform(200, 240, 150, 10, "quinta"),
                Platform(300, 150, 150, 10, "sexta"),
                Platform(300, 60, 150, 10, "setima")
            ]
        else:
            print("fim do jogo")
            self.platforms = []

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from scenes.main_menu import MainMenu
                    self.next_scene = MainMenu()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(self.platforms)  # <- só passa platforms

        # carregar fase se ainda não tiver
        if not self.platforms:
            self.setup_level(self.level)

        # limitar player horizontalmente
        screen_width = pygame.display.get_surface().get_width()
        self.player.x = max(0, min(self.player.x, screen_width - self.player.width))

        # limitar player verticalmente na primeira fase
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

        # atualizar inimigos
        for enemy in self.enemies:
            enemy.update(self.platforms, self.ground_y)

        # colisão com inimigos
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        for enemy in self.enemies:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if player_rect.colliderect(enemy_rect):
                from scenes.death_menu import DeathMenu
                self.next_scene = DeathMenu()

    def render(self, screen):
        screen.fill((20, 120, 20))

        # desenhar plataformas
        for plat in self.platforms:
            plat.draw(screen)

        # desenhar player e inimigos
        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)

        # texto
        text = self.font.render("escale", True, (255, 255, 255))
        screen.blit(text, (350, 50))