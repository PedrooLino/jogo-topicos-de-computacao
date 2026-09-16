class Animation:
    """
    Sequência de frames (Sprite) reproduzida com um intervalo fixo entre
    cada um. Uma animação com um único frame se comporta simplesmente
    como uma imagem estática (é o caso de praticamente todas as
    entidades do jogo hoje, que só têm uma imagem "parada").

    Feita para já suportar spritesheets/animação de fato no futuro,
    bastando passar mais de um caminho de imagem em
    AnimationSet.add_animation().
    """

    def __init__(self, frames, frame_duration=0.1, loop=True):
        if not frames:
            raise ValueError("Uma animação precisa de pelo menos um frame")

        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop

        self.time = 0.0
        self.current_frame = 0
        self.finished = False

    def reset(self):
        self.time = 0.0
        self.current_frame = 0
        self.finished = False

    def update(self, dt):
        if self.finished or len(self.frames) <= 1:
            return

        self.time += dt

        while self.time >= self.frame_duration:
            self.time -= self.frame_duration
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
                    break

    def get_sprite(self):
        return self.frames[self.current_frame]
