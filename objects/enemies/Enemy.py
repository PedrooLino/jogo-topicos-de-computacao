import pygame
import random
from objects.GameObject import GameObject
from objects.Projectile import Projectile
 
 
class Enemy(GameObject):
    def __init__(self, x, y, width=50, height=50, speed=2, color=(0, 0, 255)):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.speed = speed
        self.vel_y = 0
        self.gravity = 0.5
        self.jumping = False
        self.hp = 3
        self.alive = True
 
        self.color = color
 
        self.shoot_delay = 1500
        self.last_shot = pygame.time.get_ticks()
 
       
        self.drop_chance = 0.05
 
    def update(self, platforms, ground_y, projectiles_list):
        self.x += self.speed
        screen_width = pygame.display.get_surface().get_width()
 
        if self.x + self.width > screen_width or self.x < 0:
            self.speed *= -1
 
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            direction = 1 if self.speed > 0 else -1
 
            new_proj = Projectile(
                self.x + self.width // 2,
                self.y + self.height // 2,
                direction
            )
            projectiles_list.append(new_proj)
            self.last_shot = now
 
        self.vel_y += self.gravity
        self.y += self.vel_y
 
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
 
        for plat in platforms:
            if enemy_rect.colliderect(plat.rect):
                if self.vel_y > 0 and enemy_rect.bottom - self.vel_y <= plat.rect.top:
                    self.y = plat.rect.top - self.height
                    self.vel_y = 0
                    self.jumping = False
                else:
                    self.speed *= -1
                    self.x += self.speed * 2
                    enemy_rect.x = self.x
 
        if self.y + self.height >= ground_y:
            self.y = ground_y - self.height
            self.vel_y = 0
            self.jumping = False
 
    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (self.x, self.y, self.width, self.height)
        )
 
    def take_damage(self, damage=1):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
 
    def try_drop(self):
       
        if random.random() < self.drop_chance:
            from objects.Drop import Drop
            return Drop(self.x + self.width // 2, self.y)
        return None