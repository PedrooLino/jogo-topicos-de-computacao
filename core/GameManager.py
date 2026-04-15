import pygame
from scenes.main_menu import MainMenu

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        self.screen_width, self.screen_height = self.screen.get_size()
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.current_scene = MainMenu()



    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_scene.handle_events(events)
            
            self.current_scene.update()

            if self.current_scene.next_scene != self.current_scene:
                self.current_scene = self.current_scene.next_scene
            self.current_scene.next_scene = self.current_scene

            self.current_scene.render(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60) 

        pygame.quit()

if __name__ == "__main__":
    manager = GameManager()
    manager.run()