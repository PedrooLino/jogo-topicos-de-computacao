import pygame
from objects.GameObject import GameObject
from objects.Projectile import Projectile

class Player(GameObject):
    
    def __init__(self, x, y, width=50, height=50, speed=5, jump_strength=-12, gravity=0.5):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.speed = speed
        self.vel_y = 0
        self.gravity = gravity
        self.jump_strength = jump_strength
        self.jumping = False

        self.direction = 1
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()

    def handle_input(self, keys):
        self.vel_x = 0 
        if keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.direction = -1
        if keys[pygame.K_d]:
            self.vel_x = self.speed
            self.direction = 1
            
        if keys[pygame.K_w] and not self.jumping:
            self.vel_y = self.jump_strength
            self.jumping = True
            self.on_ground = False

    def update(self, platforms, ground_y=600):
        self.x += self.vel_x
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for plat in platforms:
            if hasattr(plat, "estado") and plat.estado != "normal":
                continue
            
            if player_rect.colliderect(plat.rect):
                if self.vel_x > 0:
                    self.x = plat.rect.left - self.width
                elif self.vel_x < 0:
                    self.x = plat.rect.right
                player_rect.x = self.x 

        self.vel_y += self.gravity
        self.y += self.vel_y
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.on_ground = False

        for plat in platforms:
            if hasattr(plat, "estado") and plat.estado != "normal":
                continue

            if player_rect.colliderect(plat.rect):
                if self.vel_y > 0:
                    self.y = plat.rect.top - self.height
                    self.vel_y = 0
                    self.jumping = False
                    self.on_ground = True
                    if hasattr(plat, "trigger"):
                        plat.trigger()
                elif self.vel_y < 0:
                    self.y = plat.rect.bottom
                    self.vel_y = 0

        if ground_y is not None and self.y + self.height >= ground_y:
            self.y = ground_y - self.height
            self.vel_y = 0
            self.jumping = False
            self.on_ground = True

        if not self.on_ground:
            self.jumping = True

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def shoot(self, projectiles_list):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            from objects.Projectile import Projectile
            proj = Projectile(
                self.x + self.width // 2,
                self.y + self.height // 2,
                self.direction
            )
            projectiles_list.append(proj)
            self.last_shot = now