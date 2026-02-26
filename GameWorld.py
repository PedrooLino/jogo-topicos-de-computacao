import pygame
from GameScene import GameScene

class GameWorld(GameScene):

    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 40)
        self.player_x = 100
        self.ground_y = 300      # altura do chão (y fixo)
        self.player_height = 50
        self.player_y = self.ground_y - self.player_height     # posição inicial no chão
        self.speed = 5

        # Gravidade e pulo
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.jumping = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from MainMenu import MainMenu
                    self.next_scene = MainMenu()

    def update(self):
        keys = pygame.key.get_pressed()

        # Movimento horizontal
        if keys[pygame.K_a]:
            self.player_x -= self.speed
        if keys[pygame.K_d]:
            self.player_x += self.speed

        # Pulo
        if keys[pygame.K_w] and not self.jumping:
            self.vel_y = self.jump_strength
            self.jumping = True

        # Aplica gravidade
        self.vel_y += self.gravity
        self.player_y += self.vel_y

        # Checa se bateu no chão
        if self.player_y + self.player_height >= self.ground_y:
            self.player_y = self.ground_y - self.player_height
            self.vel_y = 0
            self.jumping = False

    def render(self, screen):
        screen.fill((20, 120, 20))
        pygame.draw.rect(screen, (255, 0, 0), (self.player_x, self.player_y, 50, self.player_height))

        text = self.font.render("RUN AND GUN!", True, (255, 255, 255))
        screen.blit(text, (350, 50))