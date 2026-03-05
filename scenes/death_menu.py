import pygame
from scenes.GameScene import GameScene

class DeathMenu(GameScene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    from scenes.main_menu import MainMenu
                    self.next_scene = MainMenu()

    def update(self):
        pass

    def render(self, screen):
        screen.fill((0, 0, 0))
        text = self.font.render("Você sucumbiu a escuridão... mas ainda há esperença...", True, (255, 0, 0))
        screen.blit(text, (100, 200))

        text2 = self.font.render("Pressione ESPAÇO para tentar de novo", True, (255, 0, 0))
        screen.blit(text2, (100, 550))