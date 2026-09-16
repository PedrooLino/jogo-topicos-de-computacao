import pygame


class Sprite:

    _cache = {}

    def __init__(self, image_path, width, height):
        self.image_path = image_path
        self.width = width
        self.height = height

        self.image = self._load(image_path, width, height)
        self.image_flipped = pygame.transform.flip(self.image, True, False)

    @classmethod
    def _load(cls, image_path, width, height):
        key = (image_path, width, height)

        if key not in cls._cache:
            raw = pygame.image.load(image_path).convert_alpha()
            cls._cache[key] = pygame.transform.scale(raw, (width, height))

        return cls._cache[key]

    def get_image(self, flipped=False):
        return self.image_flipped if flipped else self.image
