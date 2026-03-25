import pygame
from objects.game_object import GameObject
from objects.projectile import Projectile

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

        self.direction = 1  # 1 = direita, -1 = esquerda
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()

    def handle_input(self, keys):
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.direction = -1
        if keys[pygame.K_d]:
            self.x += self.speed
            self.direction = 1
        if keys[pygame.K_w] and not self.jumping:
            self.vel_y = self.jump_strength
            self.jumping = True
            self.on_ground = False

    def update(self, platforms, ground_y=600):
        # aplicar gravidade
        self.vel_y += self.gravity
        previous_y = self.y
        next_y = self.y + self.vel_y
        player_rect = pygame.Rect(self.x, next_y, self.width, self.height)

        # reset do estado de chão a cada update
        self.on_ground = False

        for plat in platforms:
            # ignora plataformas quebráveis já abertas
            if hasattr(plat, "estado") and plat.estado != "normal":
                continue

            plat_rect = plat.rect

            # colisão vertical apenas se o player estava acima da plataforma
            if previous_y + self.height <= plat_rect.top and next_y + self.height >= plat_rect.top:
                if player_rect.right > plat_rect.left and player_rect.left < plat_rect.right:
                    next_y = plat_rect.top - self.height
                    self.vel_y = 0
                    self.jumping = False
                    self.on_ground = True

                    # dispara trigger de plataforma quebrável
                    if hasattr(plat, "trigger"):
                        plat.trigger()
                    break

        # colisão com o chão
        if ground_y is not None and next_y + self.height >= ground_y:
            next_y = ground_y - self.height
            self.vel_y = 0
            self.jumping = False
            self.on_ground = True

        # se não está no chão, considera que está no ar
        if not self.on_ground:
            self.jumping = True

        self.y = next_y

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def shoot(self, projectiles_list):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            from objects.projectile import Projectile
            proj = Projectile(
                self.x + self.width // 2,
                self.y + self.height // 2,
                self.direction
            )
            projectiles_list.append(proj)
            self.last_shot = now