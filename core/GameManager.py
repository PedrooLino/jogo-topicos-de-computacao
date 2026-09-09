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

        # Cria o gerenciador de cenas
        self.scene_manager = SceneManager()

        # Coloca o menu principal na pilha
        self.scene_manager.push(
            MainMenu(self.audio, self.scene_manager)
        )


    def run(self):

        while self.running:

            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT:
                    self.running = False

            # Cena que estava ativa antes dos eventos
            current_scene = self.scene_manager.current()

            current_scene.handle_events(events)

            # Pega novamente a cena atual.
            # Isso é importante porque o handle_events
            # pode ter alterado a pilha.
            current_scene = self.scene_manager.current()

            current_scene.update()
            current_scene.render(self.screen)

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()



if __name__ == "__main__":

    manager = GameManager()
    manager.run()
