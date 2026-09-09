import pygame
from scenes.GameScene import GameScene


class PauseMenu(GameScene):

    def __init__(self, audio, scene_manager):
        super().__init__()

        self.audio = audio
        self.scene_manager = scene_manager

        self.font = pygame.font.SysFont(
            "Courier New",
            24,
            bold=True
        )

        self.title_font = pygame.font.SysFont(
            "Courier New",
            60,
            bold=True
        )

        self.button_width = 300
        self.button_height = 65
        self.button_gap = 30

        self.selected_button = 0

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                # ESC = continuar
                if event.key == pygame.K_ESCAPE:
                    self.continue_game()

                elif event.key == pygame.K_UP:

                    self.selected_button = (
                        self.selected_button - 1
                    ) % 3

                elif event.key == pygame.K_DOWN:

                    self.selected_button = (
                        self.selected_button + 1
                    ) % 3

                elif event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE
                ):
                    self.activate_button()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    mouse_pos = pygame.mouse.get_pos()

                    continue_rect, menu_rect, exit_rect = (
                        self.get_button_rects()
                    )

                    if continue_rect.collidepoint(mouse_pos):
                        self.continue_game()

                    elif menu_rect.collidepoint(mouse_pos):
                        self.main_menu()

                    elif exit_rect.collidepoint(mouse_pos):
                        self.exit_game()

    def activate_button(self):

        if self.selected_button == 0:
            self.continue_game()

        elif self.selected_button == 1:
            self.main_menu()

        elif self.selected_button == 2:
            self.exit_game()

    def continue_game(self):

        self.scene_manager.pop()

    def main_menu(self):

        from scenes.MainMenu import MainMenu

        self.scene_manager.clear()

        self.scene_manager.push(
            MainMenu(
                self.audio,
                self.scene_manager
            )
        )


    def exit_game(self):

        pygame.quit()
        quit()

    def get_button_rects(self):

        screen = pygame.display.get_surface()

        screen_width, screen_height = screen.get_size()

        total_height = (
            self.button_height * 3
            + self.button_gap * 2
        )

        start_y = (
            screen_height - total_height
        ) // 2

        button_x = (
            screen_width - self.button_width
        ) // 2

        continue_rect = pygame.Rect(
            button_x,
            start_y,
            self.button_width,
            self.button_height
        )

        menu_rect = pygame.Rect(
            button_x,
            start_y
            + self.button_height
            + self.button_gap,
            self.button_width,
            self.button_height
        )

        exit_rect = pygame.Rect(
            button_x,
            start_y
            + (self.button_height + self.button_gap) * 2,
            self.button_width,
            self.button_height
        )

        return continue_rect, menu_rect, exit_rect

    def update(self):
        pass

    def render_button(
        self,
        screen,
        rect,
        text,
        selected
    ):

        mouse_pos = pygame.mouse.get_pos()

        mouse_over = rect.collidepoint(mouse_pos)

        active = mouse_over or selected

        draw_rect = rect.copy()

        if mouse_over:
            draw_rect.x -= 15

        # Sombra
        shadow_rect = draw_rect.copy()

        shadow_rect.x += 8
        shadow_rect.y += 8

        pygame.draw.rect(
            screen,
            (20, 15, 15),
            shadow_rect
        )

        if active:

            button_color = (180, 45, 45)
            border_color = (255, 220, 120)
            text_color = (255, 255, 255)

        else:

            button_color = (55, 45, 45)
            border_color = (170, 150, 120)
            text_color = (210, 210, 210)

        pygame.draw.rect(
            screen,
            button_color,
            draw_rect
        )

        pygame.draw.rect(
            screen,
            border_color,
            draw_rect,
            4
        )

        text_surf = self.font.render(
            text,
            True,
            text_color
        )

        text_rect = text_surf.get_rect(
            center=draw_rect.center
        )

        screen.blit(
            text_surf,
            text_rect
        )

        if active:

            arrow_x = draw_rect.left - 30
            arrow_y = draw_rect.centery

            pygame.draw.polygon(
                screen,
                (255, 220, 120),
                [
                    (arrow_x, arrow_y),
                    (arrow_x - 12, arrow_y - 8),
                    (arrow_x - 12, arrow_y + 8)
                ]
            )

    def render(self, screen):


        previous_scene = self.scene_manager.scenes[-2]

        previous_scene.render(screen)

        #escurece
        overlay = pygame.Surface(screen.get_size())

        overlay.set_alpha(160)

        overlay.fill((0, 0, 0))

        screen.blit(
            overlay,
            (0, 0)
        )

        # Título
        title_surf = self.title_font.render(
            "PAUSADO",
            True,
            (255, 255, 255)
        )

        title_rect = title_surf.get_rect(
            center=(
                screen.get_width() // 2,
                120
            )
        )

        screen.blit(
            title_surf,
            title_rect
        )

        continue_rect, menu_rect, exit_rect = (
            self.get_button_rects()
        )

        self.render_button(
            screen,
            continue_rect,
            "CONTINUAR",
            self.selected_button == 0
        )

        self.render_button(
            screen,
            menu_rect,
            "MENU PRINCIPAL",
            self.selected_button == 1
        )

        self.render_button(
            screen,
            exit_rect,
            "SAIR",
            self.selected_button == 2
        )
