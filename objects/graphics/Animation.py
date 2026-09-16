class Animation:


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
