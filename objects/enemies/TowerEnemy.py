from objects.enemies.Enemy import Enemy
from objects.physics.Vector2 import Vector2
from objects.Projectile import Projectile


class TowerEnemy(Enemy):
    def __init__(self, x, y,
                 image_path="sprites/DemonioTorre.png",
                 color=(0, 255, 0), audio=None):

        super().__init__(x, y, speed=0, color=color,
                         image_path=image_path, audio=audio)

        self.points = 30
        self.vel.x = 0
        self.hp = 5
        self.shoot_delay = 800
        self.drop_chance = 0.6

        self.projectile_image = "sprites/bolafogo.png"

    def update(self, platforms, ground_y, projectiles_list, dt):

        if self.can_shoot():
            cx = self.pos.x + self.width // 2
            cy = self.pos.y + self.height // 2

            projectiles_list.append(
                Projectile(cx, cy, direction=Vector2(1, 0),
                           image_path=self.projectile_image)
            )

            projectiles_list.append(
                Projectile(cx, cy, direction=Vector2(-1, 0),
                           image_path=self.projectile_image)
            )

            if self.audio:
                self.audio.play_enemy_shoot()

        self.physics_update(dt, platforms, ground_y)

    def draw(self, screen):
        # Torre não se move nem vira, sempre desenha a imagem normal.
        image = self.animations.get_image(flipped=False)
        screen.blit(image, (self.pos.x, self.pos.y))
