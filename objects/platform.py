import pygame
from objects.GameObject import GameObject


class Platform(GameObject):
    def __init__(self, x, y, width, height, name=None, quebravel=False):
        super().__init__(x, y, width, height)

        self.name = name
        self.quebravel = quebravel
        self.estado = "normal"
        self.offset = 0
        self.vel_abertura = 2

    def update(self):
        if self.estado == "abrindo":
            self.offset += self.vel_abertura
            if self.offset >= self.width // 2:
                self.estado = "aberta"

    def trigger(self):
        if self.quebravel and self.estado == "normal":
            self.estado = "abrindo"

    def draw(self, screen):
        if self.estado == "normal":
            pygame.draw.rect(screen, (150, 75, 0), self.rect)

        elif self.estado == "abrindo":
            # metade esquerda
            pygame.draw.rect(
                screen,
                (150, 75, 0),
                (self.pos.x - self.offset, self.pos.y, self.width // 2, self.height)
            )
            # metade direita
            pygame.draw.rect(
                screen,
                (150, 75, 0),
                (self.pos.x + self.width // 2 + self.offset,
                 self.pos.y, self.width // 2, self.height)
            )
