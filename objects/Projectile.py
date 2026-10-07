from objects.physics.Physicsbody import PhysicsBody
from objects.physics.Vector2 import Vector2
from objects.graphics.AnimationSet import AnimationSet

PROJ_SPEED = 420


class Projectile(PhysicsBody):

    def __init__(self, x, y, direction=None,
                 image_path="sprites/tiro.png", speed=PROJ_SPEED):
        super().__init__(x, y, width=10, height=10, use_gravity=False)

        if direction is None:
            direction = Vector2(1, 0)
        elif not isinstance(direction, Vector2):
            direction = Vector2(direction, 0)

        direction = direction.normalized() if direction.length() > 0 else Vector2(1, 0)

        self.direction = direction
        self.vel = direction * speed

        self.animations = AnimationSet()
        self.animations.add_animation(
            "default", image_path, self.width, self.height)

    def update(self, dt, *args):
        self.pos = self.pos + self.vel * dt

    def draw(self, screen):
        flipped = self.vel.x < 0
        image = self.animations.get_image(flipped)
        screen.blit(image, (self.pos.x, self.pos.y))
