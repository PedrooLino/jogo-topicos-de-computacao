import pygame
from scenes.GameScene import GameScene
from objects.player import Player
from objects.enemy import Enemy
from objects.platform import Platform

class GameWorld(GameScene):

    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 40)
        self.ground_y = 600

        # jogador e inimigos
        self.player = Player(100, self.ground_y - 50)
        self.enemies = [Enemy(400, self.ground_y - 50)]

        # fase inicial
        self.level = 0
        self.platforms = []

    def setup_level(self, level):
        """Configura plataformas da fase"""
        if level == 0:
            self.platforms = [
                Platform(150, 130, 100, 10, "pulo final"),
                Platform(180, 220, 200, 10, "plataforma1"),
                Platform(560, 280, 200, 10, "plataforma2"),
                Platform(560, 520, 200, 10, "plataforma3"),
                Platform(120, 500, 100, 10, "plataforma4"),
                Platform(370, 450, 50, 10, "plataforma5"),
                Platform(500, 370, 20, 10, "plataforma6"),
            ]
        elif level == 1:
            self.platforms = [
                Platform(200, 500, 150, 10, "bottom2"),
                Platform(450, 400, 150, 10, "mid2"),
                Platform(300, 300, 150, 10, "top2"),
                Platform(100, 200, 150, 10, "top3"),
            ]
        else:
            print("Você venceu!")  # fim do jogo
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
        self.player.update(self.platforms, self.ground_y)

        # carregar a fase inicial se ainda não tiver
        if not self.platforms:
            self.setup_level(self.level)

        # subir de fase
        if self.player.y < 0:
            self.level += 1
            self.setup_level(self.level)
            # reposicionar o player embaixo da tela
            self.player.y = self.ground_y - self.player.height

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

        # tamanho da tela dinâmico
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # limitar player
        self.player.x = max(0, min(self.player.x, screen_width - self.player.width))
        self.player.y = max(0, min(self.player.y, screen_height - self.player.height))

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