import pygame


class AudioManager:

    def __init__(self):

        pygame.mixer.init()

        self.enemy_die = self.load_sound(
            "sounds/sfx/enemy_die.wav"
        )

    def load_sound(self, path):

        try:
            return pygame.mixer.Sound(path)

        except pygame.error:
            print(f"Não foi possível carregar: {path}")
            return None

    def play_enemy_die(self):
        if self.enemy_die:
            self.enemy_die.play()
