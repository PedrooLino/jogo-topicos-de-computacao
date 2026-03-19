import pygame
from scenes.GameScene import GameScene
from objects.player import Player
from objects.enemy import Enemy

class GameWorld(GameScene):

    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 40)
        self.ground_y = 600

        self.player_projectiles = []
        self.enemy_projectiles = []
       
        self.platforms = [
            pygame.Rect(150, 220, 200, 10), 
            pygame.Rect(560, 200, 200, 10),
            pygame.Rect(560, 520, 200, 10),
            pygame.Rect(120, 500, 100, 10),
            pygame.Rect(370, 450, 50, 10),
            pygame.Rect(500, 320, 20, 10)

        ]

        self.player = Player(100, self.ground_y - 50)

        self.enemies = [
            Enemy(400, self.ground_y - 50),
            
        ]

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

        if keys[pygame.K_SPACE]:
            self.player.shoot(self.player_projectiles)

        # inimigos
        for enemy in self.enemies:
            enemy.update(self.platforms, self.ground_y, self.enemy_projectiles)

        # tiros dos inimigos
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

        # colisão com player
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)

        for proj in self.enemy_projectiles:
            if proj.get_rect().colliderect(player_rect):
                from scenes.death_menu import DeathMenu
                self.next_scene = DeathMenu()

    def render(self, screen):
        screen.fill((20, 120, 20))

        for plat in self.platforms:
            pygame.draw.rect(screen, (150, 75, 0), plat)

        self.player.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        text = self.font.render("escale", True, (255, 255, 255))
        screen.blit(text, (350, 50))

        for proj in self.player_projectiles:
            proj.draw(screen)

        for proj in self.enemy_projectiles:
            proj.draw(screen)