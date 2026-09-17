from objects.GameObject import GameObject
from objects.physics.Vector2 import Vector2
from objects.physics import Collision

GRAVITY = 1800  # px/s²


class PhysicsBody(GameObject):

    def __init__(self, x, y, width=50, height=50, use_gravity=True,
                 hitbox_offset=(0, 0), hitbox_size=None):
        super().__init__(x, y, width, height,
                         hitbox_offset=hitbox_offset,
                         hitbox_size=hitbox_size)

        self.vel = Vector2(0, 0)   # px/s
        self.use_gravity = use_gravity
        self.on_ground = False

    # ---------------- Compat vel_x/vel_y (delegam para o vetor vel) ----------------
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

    # ---------------- Física ----------------
    def apply_gravity(self, dt):
        if self.use_gravity:
            self.vel.y += GRAVITY * dt

    def resolve_x(self, platforms):
        Collision.resolve_horizontal(self, platforms)

    def resolve_y(self, platforms, ground_y=None):
        self.on_ground = Collision.resolve_vertical(self, platforms, ground_y)

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

    # ---------------- Hooks (sobrescritos por subclasses quando precisar) ----------------
    def _skip_platform(self, plat):
        if not hasattr(plat, "estado"):
            return False
        return plat.estado != "normal"

    def _on_land(self, plat):
        pass
