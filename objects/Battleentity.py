import pygame
import random
from objects.Physicsbody import PhysicsBody


class BattleEntity(PhysicsBody):
    def __init__(self, x, y, width=50, height=50,
                 hp=3, use_gravity=True, color=(255, 255, 255)):
        super().__init__(x, y, width, height, use_gravity=use_gravity)

        self.hp = hp
        self.max_hp = hp
        self.alive = True
        self.color = color

        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()

        self.drop_chance = 0.0

    def take_damage(self, damage=1):
        if not self.alive:
            return
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.on_death()

    def on_death(self):
        pass

    def can_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_delay:
            self.last_shot = now
            return True
        return False

    def try_drop(self):
        if self.drop_chance > 0 and random.random() < self.drop_chance:
            from objects.Drop import Drop
            return Drop(self.pos.x + self.width // 2, self.pos.y)
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
