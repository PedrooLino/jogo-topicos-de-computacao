import pygame
from scenes.GameScene import GameScene


class MainMenu(GameScene):
    def __init__(self, audio, scene_manager):
        super().__init__()

        self.audio = audio
        self.scene_manager = scene_manager

        self.font = pygame.font.SysFont(
            "Courier New",
            20,
            bold=True
        )

        self.title_font = pygame.font.SysFont(
            "Courier New",
            72,
            bold=True
        )

        self.background = pygame.image.load(
            "sprites/Guerra_menu.png"
        ).convert()

        self.button_width = 260
        self.button_height = 65
        self.button_gap = 35

        # Ordem dos botões: 0 = Começar, 1 = Leaderboard, 2 = Créditos, 3 = Sair
        self.num_buttons = 4

        self.selected_button = None

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    if self.selected_button is None:
                        self.selected_button = 0
                    else:
                        self.selected_button = (
                            self.selected_button - 1
                        ) % self.num_buttons

                elif event.key == pygame.K_DOWN:
                    if self.selected_button is None:
                        self.selected_button = 0
                    else:
                        self.selected_button = (
                            self.selected_button + 1
                        ) % self.num_buttons

                elif event.key == pygame.K_SPACE:
                    self.start_game()

                elif event.key == pygame.K_RETURN:
                    if self.selected_button is not None:
                        self.activate_button()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    mouse_pos = pygame.mouse.get_pos()

                    start_rect, leaderboard_rect, credits_rect, exit_rect = (
                        self.get_button_rects()
                    )

                    if start_rect.collidepoint(mouse_pos):
                        self.start_game()

                    elif leaderboard_rect.collidepoint(mouse_pos):
                        self.show_leaderboard()

                    elif credits_rect.collidepoint(mouse_pos):
                        self.show_credits()

                    elif exit_rect.collidepoint(mouse_pos):
                        self.exit_game()

    def activate_button(self):

        if self.selected_button == 0:
            self.start_game()

        elif self.selected_button == 1:
            self.show_leaderboard()

        elif self.selected_button == 2:
            self.show_credits()

        elif self.selected_button == 3:
            self.exit_game()

    def start_game(self):

        from scenes.GameWorld import GameWorld

        self.scene_manager.push(
            GameWorld(self.audio, self.scene_manager)
        )

    def show_leaderboard(self):

        from scenes.LeaderboardScene import LeaderboardScene

        self.scene_manager.push(
            LeaderboardScene(
                self.audio,
                self.scene_manager
            )
        )

    def show_credits(self):

        from scenes.CreditsScene import CreditsScene

        self.scene_manager.push(
            CreditsScene(
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
            self.button_height * self.num_buttons
            + self.button_gap * (self.num_buttons - 1)
        )

        start_y = (
            screen_height - total_height
        ) // 2

        button_x = int(screen_width * 0.18)

        start_rect = pygame.Rect(
            button_x,
            start_y,
            self.button_width,
            self.button_height
        )

        leaderboard_rect = pygame.Rect(
            button_x,
            start_y
            + (self.button_height + self.button_gap) * 1,
            self.button_width,
            self.button_height
        )

        credits_rect = pygame.Rect(
            button_x,
            start_y
            + (self.button_height + self.button_gap) * 2,
            self.button_width,
            self.button_height
        )

        exit_rect = pygame.Rect(
            button_x,
            start_y
            + (self.button_height + self.button_gap) * 3,
            self.button_width,
            self.button_height
        )

        return start_rect, leaderboard_rect, credits_rect, exit_rect

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

        screen_width, screen_height = screen.get_size()

        background_scaled = pygame.transform.scale(
            self.background,
            (screen_width, screen_height)
        )

        screen.blit(
            background_scaled,
            (0, 0)
        )

        title_surf = self.title_font.render(
            "GUERRA",
            True,
            (255, 255, 255)
        )

        title_rect = title_surf.get_rect(
            topleft=(120, 80)
        )

        screen.blit(
            title_surf,
            title_rect
        )

        start_rect, leaderboard_rect, credits_rect, exit_rect = (
            self.get_button_rects()
        )

        self.render_button(
            screen,
            start_rect,
            "COMEÇAR",
            self.selected_button == 0
        )

        self.render_button(
            screen,
            leaderboard_rect,
            "LEADERBOARD",
            self.selected_button == 1
        )

        self.render_button(
            screen,
            credits_rect,
            "CRÉDITOS",
            self.selected_button == 2
        )

        self.render_button(
            screen,
            exit_rect,
            "SAIR",
            self.selected_button == 3
        )
