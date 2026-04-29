import pygame
from scenes.GameScene import GameScene

class MainMenu(GameScene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 32)
        self.title_font = pygame.font.SysFont("Arial", 64)
        self.background = pygame.image.load("sprites/Guerra_menu.png").convert()
        self.background = pygame.transform.scale(self.background, (800, 600))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    from scenes.GameWorld import GameWorld
                    self.next_scene = GameWorld()

    def update(self):
        pass

    def render(self, screen):
        screen_width, screen_height = screen.get_size()
        background_scaled = pygame.transform.scale(
            self.background,
            (screen_width, screen_height)
        )

        screen.blit(background_scaled, (0, 0))
        
        title_surf = self.title_font.render("Guerra", True, (255, 255, 255))
        screen.blit(title_surf, (150, 150))
        
        description_surf = self.font.render("Suba até o topo... cuidado com os monstros...", True, (200, 200, 200))
        screen.blit(description_surf, (150, 300))

        hint_surf = self.font.render("Pressione ESPAÇO para começar a escalada...", True, (200, 200, 200))
        screen.blit(hint_surf, (150, 500))
