import pygame
from scenes.GameScene import GameScene
from objects.player import Player
from objects.enemy import Enemy

class GameWorld(GameScene):

    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 40)
        self.ground_y = 600

        # Plataformas (x, y, largura, altura)
        self.platforms = [
            pygame.Rect(150, 220, 200, 10),
            pygame.Rect(560, 200, 200, 10),
            pygame.Rect(560, 520, 200, 10),
            pygame.Rect(120, 500, 100, 10),
            pygame.Rect(370, 450, 50, 10)
        ]

        # Player
        self.player = Player(100, self.ground_y - 50)

        # Lista de inimigos
        self.enemies = [
            Enemy(400, self.ground_y - 50),
            #Enemy(700, self.ground_y - 50)
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from scenes.main_menu import MainMenu
                    self.next_scene = MainMenu()

    def update(self):
        # Atualiza o player
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(self.platforms, self.ground_y)

        # Atualiza todos os inimigos
        for enemy in self.enemies:
            enemy.update(self.platforms, self.ground_y)

        # Verifica colisão com inimigos
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)

        for enemy in self.enemies:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if player_rect.colliderect(enemy_rect):
                from scenes.death_menu import DeathMenu
                self.next_scene = DeathMenu()

    def render(self, screen):
        # Fundo
        screen.fill((20, 120, 20))

        # Desenha plataformas
        for plat in self.platforms:
            pygame.draw.rect(screen, (150, 75, 0), plat)

        # Desenha player
        self.player.draw(screen)

        # Desenha inimigos
        for enemy in self.enemies:
            enemy.draw(screen)

        # Texto exemplo
        text = self.font.render("escale", True, (255, 255, 255))
        screen.blit(text, (350, 50))