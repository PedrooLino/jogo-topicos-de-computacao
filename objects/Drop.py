from objects.physics.Physicsbody import PhysicsBody
from objects.graphics.Sprite import Sprite


class Drop(PhysicsBody):
    def __init__(self, x, y):
        super().__init__(x, y, width=20, height=20, use_gravity=True)

        self.sprite = Sprite("sprites/drop.png", self.width, self.height)

    def update(self, platforms, ground_y, dt):
        self.physics_update(dt, platforms, ground_y)

    def draw(self, screen):
        screen.blit(self.sprite.get_image(), (self.pos.x, self.pos.y))
