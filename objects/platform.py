import pygame

class Platform:
    def __init__(self, x, y, width, height, name=None, quebravel=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.quebravel = quebravel
        self.estado = "normal" 
        self.offset = 0
        self.vel_abertura = 2

    def update(self):
        if self.estado == "abrindo":
            self.offset += self.vel_abertura
            if self.offset >= self.rect.width // 2:
                self.estado = "aberta" 

    def trigger(self):
        if self.quebravel and self.estado == "normal":
            self.estado = "abrindo"

    def draw(self, screen):
        if self.estado == "normal":
            pygame.draw.rect(screen, (150, 75, 0), self.rect)
        elif self.estado == "abrindo":
            #metade da esquerda
            pygame.draw.rect(
                screen,
                (150, 75, 0),
                (self.rect.x - self.offset, self.rect.y, self.rect.width // 2, self.rect.height)
            )
            # metade da direita
            pygame.draw.rect(
                screen,
                (150, 75, 0),
                (self.rect.x + self.rect.width // 2 + self.offset, self.rect.y, self.rect.width // 2, self.rect.height)
            )