import pygame
from scenes.GameScene import GameScene
from objects.player import Player

class GameWorld(GameScene):

    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 40)
        self.ground_y = 300

        # Plataformas
        self.platforms = [
            pygame.Rect(150, 220, 200, 20),
            pygame.Rect(560, 200, 200, 20)
        ]

        # Player como objeto
        self.player = Player(100, self.ground_y - 50)

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

    def render(self, screen):
        screen.fill((20, 120, 20))
        self.player.draw(screen)

        text = self.font.render("avance", True, (255, 255, 255))
        screen.blit(text, (350, 50))

        for plat in self.platforms:
            pygame.draw.rect(screen, (150, 75, 0), plat)