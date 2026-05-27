import pygame


class GameObject:

    def __init__(self, x, y, width=0, height=0):

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.vel_x = 0
        self.vel_y = 0

        self.gravity = 0

        self.on_ground = False

    @property
    def rect(self):

        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def apply_gravity(self):

        if self.gravity:
            self.vel_y += self.gravity

    def move(self):

        self.x += self.vel_x
        self.y += self.vel_y

    def collide_x(self, platforms):

        r = self.rect

        for p in platforms:

            if r.colliderect(p.rect):

                if self.vel_x > 0:
                    self.x = p.rect.left - self.width

                elif self.vel_x < 0:
                    self.x = p.rect.right

                r = self.rect

    def collide_y(self, platforms):

        r = self.rect

        self.on_ground = False

        for p in platforms:

            if r.colliderect(p.rect):

                if self.vel_y > 0:

                    self.y = p.rect.top - self.height

                    self.vel_y = 0

                    self.on_ground = True

                elif self.vel_y < 0:

                    self.y = p.rect.bottom

                    self.vel_y = 0

                r = self.rect

    def update(self, platforms=None):

        self.apply_gravity()

        self.move()

        if platforms:

            self.collide_x(platforms)

            self.collide_y(platforms)

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            self.rect
        )
