from objects.graphics.Sprite import Sprite
from objects.graphics.Animation import Animation


class AnimationSet:
    """
    Conjunto nomeado de animações (ex: "idle", "walk", "attack") de uma
    entidade, com troca de estado (play) e espelhamento automático
    conforme a direção em que a entidade está olhando.

    Uso típico (uma imagem estática, como hoje no jogo):

        self.animations = AnimationSet()
        self.animations.add_animation("idle", "sprites/Demonio.png",
                                       self.width, self.height)

        # no draw():
        image = self.animations.get_image(flipped=self.vel.x <= 0)
        screen.blit(image, (self.pos.x, self.pos.y))

    Uso com múltiplos frames (spritesheet futura):

        self.animations.add_animation(
            "walk",
            ["sprites/walk_0.png", "sprites/walk_1.png", "sprites/walk_2.png"],
            self.width, self.height,
            frame_duration=0.12,
        )
    """

    def __init__(self):
        self.animations = {}
        self.current_name = None

    def add_animation(self, name, image_paths, width, height,
                      frame_duration=0.1, loop=True):
        if isinstance(image_paths, str):
            image_paths = [image_paths]

        frames = [Sprite(path, width, height) for path in image_paths]
        self.animations[name] = Animation(frames, frame_duration, loop)

        if self.current_name is None:
            self.current_name = name

    def play(self, name, restart_if_same=False):
        if name not in self.animations:
            raise KeyError(f"Animação '{name}' não existe neste AnimationSet")

        if name != self.current_name or restart_if_same:
            self.animations[name].reset()

        self.current_name = name

    @property
    def current(self):
        return self.animations[self.current_name]

    def update(self, dt):
        if self.current_name is not None:
            self.current.update(dt)

    def get_image(self, flipped=False):
        return self.current.get_sprite().get_image(flipped)
