import pygame
from scenes.GameScene import GameScene


class CreditsScene(GameScene):

    def __init__(self, audio, scene_manager):
        super().__init__()

        self.audio = audio
        self.scene_manager = scene_manager

        self.font = pygame.font.SysFont(
            "Courier New",
            28,
            bold=True
        )

        self.title_font = pygame.font.SysFont(
            "Courier New",
            60,
            bold=True
        )

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.go_back()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    self.go_back()

    def go_back(self):

        self.scene_manager.pop()

    def update(self):
        pass

    def render(self, screen):

        screen.fill((0, 0, 0))

        title_surf = self.title_font.render(
            "CRÉDITOS",
            True,
            (255, 220, 120)
        )

        title_rect = title_surf.get_rect(
            center=(
                screen.get_width() // 2,
                150
            )
        )

        screen.blit(
            title_surf,
            title_rect
        )

        dev1_surf = self.font.render(
            "THEO",
            True,
            (255, 255, 255)
        )

        dev1_rect = dev1_surf.get_rect(
            center=(
                screen.get_width() // 2,
                300
            )
        )

        screen.blit(
            dev1_surf,
            dev1_rect
        )

        dev2_surf = self.font.render(
            "PEDRO LINO",
            True,
            (255, 255, 255)
        )

        dev2_rect = dev2_surf.get_rect(
            center=(
                screen.get_width() // 2,
                370
            )
        )

        screen.blit(
            dev2_surf,
            dev2_rect
        )

        back_surf = self.font.render(
            "ESC ou clique para voltar",
            True,
            (170, 170, 170)
        )

        back_rect = back_surf.get_rect(
            center=(
                screen.get_width() // 2,
                600
            )
        )

        screen.blit(
            back_surf,
            back_rect
        )
