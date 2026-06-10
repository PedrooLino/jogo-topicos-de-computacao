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
        
        self.fill_color = (30, 30, 30)
        self.border_color = (0, 0, 0)

        self.border_thickness = 2

    def update(self):
        if self.estado == "abrindo":
            self.offset += self.vel_abertura
            if self.offset >= self.width // 2:
                self.estado = "aberta"

    def trigger(self):
        if self.quebravel and self.estado == "normal":
            self.estado = "abrindo"

    def draw_block(self, screen, x, y, w, h):

        rect = pygame.Rect(int(x), int(y), int(w), int(h))

        pygame.draw.rect(screen, self.fill_color, rect)

        pygame.draw.rect(
            screen,
            self.border_color,
            rect,
            self.border_thickness
        )

    def draw(self, screen):

        if self.estado == "normal":

            self.draw_block(
                screen,
                self.pos.x,
                self.pos.y,
                self.width,
                self.height
            )

        elif self.estado == "abrindo":

            self.draw_block(
                screen,
                self.pos.x - self.offset,
                self.pos.y,
                self.width // 2,
                self.height
            )

            self.draw_block(
                screen,
                self.pos.x + self.width // 2 + self.offset,
                self.pos.y,
                self.width // 2,
                self.height
            )
