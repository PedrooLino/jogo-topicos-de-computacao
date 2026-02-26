import pygame
from GameScene import GameScene

class GameWorld(GameScene):

    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 40)
        self.player_x = 100
        self.player_y = 300
        self.speed = 5

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from MainMenu import MainMenu
                    self.next_scene = MainMenu()

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.player_x -= self.speed
        if keys[pygame.K_d]:
            self.player_x += self.speed

    def render(self, screen):
        screen.fill((20, 120, 20))
        pygame.draw.rect(screen, (255, 0, 0), (self.player_x, self.player_y, 50, 50))

        text = self.font.render("RUN AND GUN!", True, (255, 255, 255))
        screen.blit(text, (350, 50))