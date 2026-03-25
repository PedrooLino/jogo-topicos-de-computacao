import pygame
from objects.game_object import GameObject
from objects.projectile import Projectile

class Enemy(GameObject):
    def __init__(self, x, y, width=50, height=50, speed=2):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.speed = speed
        self.vel_y = 0
        self.gravity = 0.5
        self.jumping = False

        self.shoot_delay = 1500 
        self.last_shot = pygame.time.get_ticks()

    def update(self, platforms, ground_y, projectiles_list):
       
        self.x += self.speed
        if self.x + self.width > 800 or self.x < 0: 
            self.speed *= -1

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            direction = 1 if self.speed > 0 else -1
           
            from objects.projectile import Projectile 
            new_proj = Projectile(self.x + self.width//2, self.y + self.height//2, direction)
            projectiles_list.append(new_proj)
            self.last_shot = now

       
        self.vel_y += self.gravity
        self.y += self.vel_y

        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for plat in platforms:
            plat_rect = plat.rect  # <- aqui pegamos o rect do objeto Platform
            if (enemy_rect.bottom - self.vel_y <= plat_rect.top and
                enemy_rect.bottom >= plat_rect.top and
                enemy_rect.right > plat_rect.left and
                enemy_rect.left < plat_rect.right):
                self.y = plat_rect.top - self.height
                self.vel_y = 0
                self.jumping = False

        if self.y + self.height >= ground_y:
            self.y = ground_y - self.height
            self.vel_y = 0
            self.jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))