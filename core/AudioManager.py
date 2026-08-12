import pygame


class AudioManager:

    def __init__(self):
        pygame.mixer.init()

        
        self.background_music = "sounds/background.mp3"
        self.enemy_die = self.load_sound("sounds/sfx/morteInimigo.mp3")
        self.player_shoot = self.load_sound("sounds/sfx/tiro.mp3")
        self.enemy_shoot = self.load_sound("sounds/sfx/fireball.mp3")

    def load_sound(self, path):
        try:
            return pygame.mixer.Sound(path)
        except pygame.error:
            print(f"Não foi possível carregar: {path}")
            return None

    def play_background_music(self):
        try:
            pygame.mixer.music.load(self.background_music)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except pygame.error:
            print(
                f"Não foi possível reproduzir a música: {self.background_music}")

    def play_enemy_die(self):
        if self.enemy_die:
            self.enemy_die.play()

    def play_player_shoot(self):
        if self.player_shoot:
            self.player_shoot.play()

    def play_enemy_shoot(self):
        if self.enemy_shoot:
            self.enemy_shoot.play()
