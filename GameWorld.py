import pygame
from GameScene import GameScene

class GameWorld(GameScene):

    def __init__(self):
        # Plataforma fixa (x, y, largura, altura)
        self.platforms = [
            pygame.Rect(150, 250, 200, 20)  # plataforma em x=400, y=400, largura=200, altura=20
        ]

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

        # Inicialmente, assume que não está em plataforma/chão
        on_ground_or_platform = False

        # Cria retângulo do player
        player_rect = pygame.Rect(self.player_x, self.player_y, 50, self.player_height)

        for plat in self.platforms:
            plat_rect = plat
            # Checa colisão vertical **e horizontal**
            if (player_rect.bottom - self.vel_y <= plat_rect.top and  # estava acima da plataforma
                player_rect.bottom >= plat_rect.top and               # caiu neste frame
                player_rect.right > plat_rect.left and               # está dentro da largura da plataforma
                player_rect.left < plat_rect.right):                 # está dentro da largura da plataforma
                # Ajusta player em cima da plataforma
                self.player_y = plat_rect.top - self.player_height
                self.vel_y = 0
                self.jumping = False
                on_ground_or_platform = True

        # Checa colisão com o chão
        if self.player_y + self.player_height >= self.ground_y:
            self.player_y = self.ground_y - self.player_height
            self.vel_y = 0
            self.jumping = False
            on_ground_or_platform = True

    def render(self, screen):
        screen.fill((20, 120, 20))
        pygame.draw.rect(screen, (255, 0, 0), (self.player_x, self.player_y, 50, self.player_height))

        text = self.font.render("RUN AND GUN!", True, (255, 255, 255))
        screen.blit(text, (350, 50))

        for plat in self.platforms:
            pygame.draw.rect(screen, (150, 75, 0), plat)  # marrom