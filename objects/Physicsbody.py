import pygame
from objects.GameObject import GameObject
from objects.Vector2 import Vector2

GRAVITY = 1800  # px/s²


class PhysicsBody(GameObject):
    """
    Física baseada em delta time.
    pos e vel são Vector2. Toda lógica de gravidade, movimento e
    resolução de colisão vive aqui.
    """

    def __init__(self, x, y, width=50, height=50, use_gravity=True):
        super().__init__(x, y, width, height)

        self.vel = Vector2(0, 0)   # px/s
        self.use_gravity = use_gravity
        self.on_ground = False

    # ------------------------------------------------------------------ #
    #  Atalhos de compatibilidade para vel_x / vel_y                      #
    # ------------------------------------------------------------------ #

    @property
    def vel_x(self):
        return self.vel.x

    @vel_x.setter
    def vel_x(self, value):
        self.vel.x = float(value)

    @property
    def vel_y(self):
        return self.vel.y

    @vel_y.setter
    def vel_y(self, value):
        self.vel.y = float(value)

    # ------------------------------------------------------------------ #
    #  Física                                                              #
    # ------------------------------------------------------------------ #

    def apply_gravity(self, dt):
        if self.use_gravity:
            self.vel.y += GRAVITY * dt

    def resolve_x(self, platforms):
        rect = self.rect
        for plat in platforms:
            if self._skip_platform(plat):
                continue
            if rect.colliderect(plat.rect):
                if self.vel.x > 0:
                    self.pos.x = plat.rect.left - self.width
                elif self.vel.x < 0:
                    self.pos.x = plat.rect.right
                rect = self.rect

    def resolve_y(self, platforms, ground_y=None):
        self.on_ground = False
        rect = self.rect

        for plat in platforms:
            if self._skip_platform(plat):
                continue
            if rect.colliderect(plat.rect):
                if self.vel.y > 0:
                    self.pos.y = plat.rect.top - self.height
                    self.vel.y = 0
                    self.on_ground = True
                    self._on_land(plat)
                elif self.vel.y < 0:
                    self.pos.y = plat.rect.bottom
                    self.vel.y = 0
                rect = self.rect

        if ground_y is not None and self.pos.y + self.height >= ground_y:
            self.pos.y = ground_y - self.height
            self.vel.y = 0
            self.on_ground = True

    def physics_update(self, dt, platforms=None, ground_y=None):
        """Move X → resolve X → move Y → resolve Y."""
        self.apply_gravity(dt)

        self.pos.x += self.vel.x * dt
        if platforms:
            self.resolve_x(platforms)

        self.pos.y += self.vel.y * dt
        if platforms:
            self.resolve_y(platforms, ground_y)
        elif ground_y is not None:
            if self.pos.y + self.height >= ground_y:
                self.pos.y = ground_y - self.height
                self.vel.y = 0
                self.on_ground = True

    # ------------------------------------------------------------------ #
    #  Hooks                                                               #
    # ------------------------------------------------------------------ #

    def _skip_platform(self, plat):
        if not hasattr(plat, "estado"):
            return False
        return plat.estado != "normal"

    def _on_land(self, plat):
        pass
