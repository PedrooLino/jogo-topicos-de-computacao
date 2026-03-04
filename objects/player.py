import pygame
from objects.game_object import GameObject

class Player(GameObject):
    def __init__(self, x, y, width=50, height=50, speed=5, jump_strength=-10, gravity=0.5):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.speed = speed
        self.vel_y = 0
        self.gravity = gravity
        self.jump_strength = jump_strength
        self.jumping = False

    def handle_input(self, keys):
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_w] and not self.jumping:
            self.vel_y = self.jump_strength
            self.jumping = True

    def update(self, platforms, ground_y):
        self.vel_y += self.gravity
        self.y += self.vel_y

        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for plat in platforms:
            if (player_rect.bottom - self.vel_y <= plat.top and
                player_rect.bottom >= plat.top and
                player_rect.right > plat.left and
                player_rect.left < plat.right):
                self.y = plat.top - self.height
                self.vel_y = 0
                self.jumping = False

        if self.y + self.height >= ground_y:
            self.y = ground_y - self.height
            self.vel_y = 0
            self.jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))