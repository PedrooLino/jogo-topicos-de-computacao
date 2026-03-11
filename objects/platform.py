import pygame

class Platform:
    def __init__(self, x, y, width, height, name=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name  # opcional, útil para depuração

    def draw(self, screen):
        pygame.draw.rect(screen, (150, 75, 0), self.rect)