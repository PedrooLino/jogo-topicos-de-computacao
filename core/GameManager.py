import pygame

from scenes.MainMenu import MainMenu
from core.AudioManager import AudioManager
from core.SceneManager import SceneManager


class GameManager:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN
        )

        self.screen_width, self.screen_height = (
            self.screen.get_size()
        )

        self.clock = pygame.time.Clock()
        self.running = True

        self.audio = AudioManager()

        self.scene_manager = SceneManager()
        
        
        
        self.scene_manager.push(
            MainMenu(self.audio, self.scene_manager)
        )


    def run(self):

        while self.running:

            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT:
                    self.running = False

            current_scene = self.scene_manager.current()

            current_scene.handle_events(events)


            current_scene = self.scene_manager.current()

            current_scene.update()
            current_scene.render(self.screen)

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()



if __name__ == "__main__":

    manager = GameManager()
    manager.run()
