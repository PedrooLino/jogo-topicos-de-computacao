import pygame
from MainMenu import MainMenu

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Começamos com o Menu Principal
        self.current_scene = MainMenu()

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            # 1. Delega os eventos para a cena atual
            self.current_scene.handle_events(events)
            
            # 2. Atualiza a lógica da cena
            self.current_scene.update()
            
            # 3. Verifica se a cena quer mudar (Troca de Menu -> Jogo)
            if self.current_scene.next_scene != self.current_scene:
                self.current_scene = self.current_scene.next_scene

            # 4. Renderiza
            self.current_scene.render(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60) # Mantém 60 FPS

        pygame.quit()

# Para rodar:
if __name__ == "__main__":
    manager = GameManager()
    manager.run()