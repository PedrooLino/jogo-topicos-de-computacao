import pygame
from scenes.GameScene import GameScene

class MainMenu(GameScene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 32)
        self.title_font = pygame.font.SysFont("Arial", 64)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    from scenes.GameWorld import GameWorld
                    self.next_scene = GameWorld()

    def update(self):
        pass

    def render(self, screen):
        screen.fill((30, 30, 60)) # Fundo azul escuro
        
        # Texto do Título
        title_surf = self.title_font.render("Guerra", True, (255, 255, 255))
        screen.blit(title_surf, (150, 150))
        
        # Instrução
        hint_surf = self.font.render("Pressione ESPAÇO para Iniciar", True, (200, 200, 200))
        screen.blit(hint_surf, (160, 300))