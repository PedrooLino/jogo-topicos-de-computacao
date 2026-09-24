import pygame
from scenes.GameScene import GameScene
from core.Leaderboard import Leaderboard


class LeaderboardScene(GameScene):
    """
    Tela exclusiva do ranking (estilo arcade). Mostra até 10 posições
    com nome de 3 letras + pontuação. Sai com ESC/ENTER/SPACE, ou
    clicando no botão "VOLTAR".

    Pode ser aberta a partir do MainMenu, do DeathMenu ou do
    VictoryMenu — o "voltar" sempre retorna pra cena que a chamou,
    já que ela é apenas empilhada por cima (scene_manager.pop()).
    """

    def __init__(self, audio, scene_manager):
        super().__init__()

        self.audio = audio
        self.scene_manager = scene_manager

        self.leaderboard = Leaderboard()

        self.title_font = pygame.font.SysFont("Courier New", 50, bold=True)
        self.header_font = pygame.font.SysFont("Courier New", 22, bold=True)
        self.row_font = pygame.font.SysFont("Courier New", 26, bold=True)
        self.hint_font = pygame.font.SysFont("Courier New", 18, bold=True)

        self.button_width = 240
        self.button_height = 55

    # ------------------------------------------------------------------ #

    def handle_events(self, events):
        for event in events:

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                    self.go_back()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.get_back_rect().collidepoint(pygame.mouse.get_pos()):
                        self.go_back()

    def go_back(self):
        self.scene_manager.pop()

    def get_back_rect(self):
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_size()

        return pygame.Rect(
            (screen_width - self.button_width) // 2,
            screen_height - 110,
            self.button_width,
            self.button_height
        )

    def update(self):
        pass

    # ------------------------------------------------------------------ #

    def render(self, screen):
        screen.fill((10, 10, 15))

        screen_width, _ = screen.get_size()

        title_surf = self.title_font.render("RANKING", True, (255, 220, 120))
        title_rect = title_surf.get_rect(center=(screen_width // 2, 90))
        screen.blit(title_surf, title_rect)

        header_surf = self.header_font.render(
            "POS   NOME       PONTOS", True, (200, 200, 200)
        )
        header_rect = header_surf.get_rect(center=(screen_width // 2, 155))
        screen.blit(header_surf, header_rect)

        entries = self.leaderboard.top_entries()

        start_y = 205
        row_gap = 40

        if not entries:
            empty_surf = self.row_font.render(
                "NENHUM RECORDE AINDA", True, (150, 150, 150)
            )
            empty_rect = empty_surf.get_rect(
                center=(screen_width // 2, start_y + 40)
            )
            screen.blit(empty_surf, empty_rect)

        for i, entry in enumerate(entries):
            position = i + 1

            color = (255, 220, 120) if position <= 3 else (220, 220, 220)

            row_text = f"{position:>2}o    {entry['name']:<3}        {entry['score']}"

            row_surf = self.row_font.render(row_text, True, color)
            row_rect = row_surf.get_rect(
                center=(screen_width // 2, start_y + i * row_gap)
            )
            screen.blit(row_surf, row_rect)

        # ---------------- Botão voltar ----------------
        back_rect = self.get_back_rect()

        mouse_pos = pygame.mouse.get_pos()
        hovered = back_rect.collidepoint(mouse_pos)

        pygame.draw.rect(
            screen,
            (180, 45, 45) if hovered else (55, 45, 45),
            back_rect
        )
        pygame.draw.rect(screen, (170, 150, 120), back_rect, 3)

        back_text = self.header_font.render("VOLTAR", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)

        hint_surf = self.hint_font.render(
            "ESC / ENTER para voltar", True, (140, 140, 140)
        )
        hint_rect = hint_surf.get_rect(
            center=(screen_width // 2, back_rect.bottom + 30)
        )
        screen.blit(hint_surf, hint_rect)
