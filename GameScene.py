import pygame

class GameScene:
    def __init__(self):
        self.next_scene = self 

    def handle_events(self, events):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self, screen):
        raise NotImplementedError