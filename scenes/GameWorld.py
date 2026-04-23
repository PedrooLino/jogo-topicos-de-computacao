import pygame
from scenes.GameScene import GameScene
from objects.player import Player
from objects.enemy import Enemy
from objects.platform import Platform
from levels.levels import LEVELS

class GameWorld(GameScene):

    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 40)
        self.ground_y = 1000

        self.player_projectiles = []
        self.enemy_projectiles = []

        self.player = Player(100, self.ground_y - 50)
        

        self.level = 0
        self.platforms = []
        self.enemies = []
        self.setup_level(self.level)

        

       

    def setup_level(self, level):
        self.platforms = []
        self.enemies = []

        if level not in LEVELS:
            print("Fim do jogo")
            return

        for data in LEVELS[level]:
            self.platforms.append(Platform(*data))

        if level == 0:
            self.enemies.append(Enemy(500, 800))
        if level == 0:
            self.enemies.append(Enemy(600, 800))

    def update(self):
        keys = pygame.key.get_pressed()

        self.handle_player_input(keys)
        self.update_platforms()
        self.update_player()
        self.update_enemies()
        self.update_projectiles()
        self.check_collisions()
        self.handle_level_transitions()

    def handle_player_input(self, keys):
        self.player.handle_input(keys)
        if keys[pygame.K_SPACE]:
            self.player.shoot(self.player_projectiles)

    def update_platforms(self):
        for plat in self.platforms:
            plat.update()

    def update_player(self):
        ground_y = self.ground_y if self.level == 0 else None
        self.player.update(self.platforms, ground_y)

        

        # limitar na tela
        screen_width = pygame.display.get_surface().get_width()
        self.player.x = max(0, min(self.player.x, screen_width - self.player.width))

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update(self.platforms, self.ground_y, self.enemy_projectiles)

    def update_projectiles(self):
        screen_width = pygame.display.get_surface().get_width()
        # inimigos
        for proj in self.enemy_projectiles[:]:
            proj.update()
            if proj.x < 0 or proj.x > screen_width:
                self.enemy_projectiles.remove(proj)

        # player
        for proj in self.player_projectiles[:]:
            proj.update()

            hit = False  

            for enemy in self.enemies:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)

                if proj.get_rect().colliderect(enemy_rect):
                    enemy.take_damage(1)
                    hit = True
                    break  

            if hit:
                if proj in self.player_projectiles:
                    self.player_projectiles.remove(proj)


        # Para os projéteis do Player
        for proj in self.player_projectiles[:]:
            proj_rect = proj.get_rect()
            for plat in self.platforms:
                if proj_rect.colliderect(plat.rect):
                    if proj in self.player_projectiles:
                        self.player_projectiles.remove(proj)
                    break 

        # Para os projéteis dos Inimigos
        for proj in self.enemy_projectiles[:]:
            proj_rect = proj.get_rect()
            for plat in self.platforms:
                if proj_rect.colliderect(plat.rect):
                    if proj in self.enemy_projectiles:
                        self.enemy_projectiles.remove(proj)
                    break

    def check_collisions(self):
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)

        for proj in self.enemy_projectiles[:]:
            if proj.get_rect().colliderect(player_rect):
                from scenes.death_menu import DeathMenu
                self.next_scene = DeathMenu()
                return

        for enemy in self.enemies:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if player_rect.colliderect(enemy_rect):
                from scenes.death_menu import DeathMenu
                self.next_scene = DeathMenu()
                return
            
        # remover inimigos mortos o
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]

    def handle_level_transitions(self):
        if self.player.y < 0:
            self.level += 1
            self.setup_level(self.level)
            self.player.y = self.ground_y - self.player.height

        elif self.player.y > self.ground_y and self.level > 0:
            self.level -= 1
            self.setup_level(self.level)
            self.player.y = 0

        if self.level == 0 and self.player.y + self.player.height > self.ground_y:
            self.player.y = self.ground_y - self.player.height
            self.player.vel_y = 0
            self.player.jumping = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from scenes.main_menu import MainMenu
                self.next_scene = MainMenu()

    def render(self, screen):
        screen.fill((20, 120, 20))

        for plat in self.platforms:
            plat.draw(screen)

        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)

        for proj in self.player_projectiles:
            proj.draw(screen)

        for proj in self.enemy_projectiles:
            proj.draw(screen)

        # texto pa marca a fase q ta
        text = self.font.render(f"Fase: {self.level}", True, (255, 255, 255))
        screen.blit(text, (350, 50))