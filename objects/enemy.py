import pygame
from objects.game_object import GameObject

class Enemy(GameObject):
    def __init__(self, x, y, width=50, height=50, speed=2):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.speed = speed
        self.vel_y = 0
        self.gravity = 0.5
        self.jumping = False

    def update(self, platforms, ground_y):
        # Exemplo de movimentação simples: vai e volta horizontalmente
        self.x += self.speed
        if self.x + self.width > 800 or self.x < 0:  # Limites da tela
            self.speed *= -1

        # Gravidade e colisão com chão/plataformas
        self.vel_y += self.gravity
        self.y += self.vel_y

        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for plat in platforms:
            if (enemy_rect.bottom - self.vel_y <= plat.top and
                enemy_rect.bottom >= plat.top and
                enemy_rect.right > plat.left and
                enemy_rect.left < plat.right):
                self.y = plat.top - self.height
                self.vel_y = 0
                self.jumping = False

        if self.y + self.height >= ground_y:
            self.y = ground_y - self.height
            self.vel_y = 0
            self.jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))