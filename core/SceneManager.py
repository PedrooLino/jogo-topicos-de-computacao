class SceneManager:

    def __init__(self):
        self.scenes = []

    def push(self, scene):
        self.scenes.append(scene)

    def pop(self):
        if len(self.scenes) > 1:
            self.scenes.pop()

    def clear(self):
        self.scenes.clear()

    def current(self):
        return self.scenes[-1]
