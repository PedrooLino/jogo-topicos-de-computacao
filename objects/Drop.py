import pygame
 
 
class Drop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
 
        self.vel_y = 0
        self.gravity = 0.4
 
    def update(self, platforms, ground_y):
        self.vel_y += self.gravity
        self.y += self.vel_y
 
        rect = self.get_rect()
 
        for plat in platforms:
            if rect.colliderect(plat.rect):
                if self.vel_y > 0 and rect.bottom - self.vel_y <= plat.rect.top:
                    self.y = plat.rect.top - self.height
                    self.vel_y = 0
                    break
 
        if ground_y is not None and self.y + self.height >= ground_y:
            self.y = ground_y - self.height
            self.vel_y = 0
 
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
 
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 215, 0), self.get_rect(), border_radius=4)
 