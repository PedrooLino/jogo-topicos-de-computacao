import pygame
from scenes.GameScene import GameScene
from core.Leaderboard import Leaderboard

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class NameEntryScene(GameScene):
    """
    Tela clássica de "digite seu nome" dos arcades: exatamente 3
    letras, cada uma escolhida com CIMA/BAIXO, navegando entre as
    posições com ESQUERDA/DIREITA, e confirmando com ENTER/SPACE.

    `next_scene_factory` é uma função sem argumentos que cria a cena
    a mostrar depois de salvar o nome no ranking (normalmente uma
    lambda que cria a VictoryMenu). Isso evita que este arquivo
    precise importar VictoryMenu diretamente.
    """

    def __init__(self, audio, scene_manager, score, next_scene_factory):
        super().__init__()

        self.audio = audio
        self.scene_manager = scene_manager
        self.score = score
        self.next_scene_factory = next_scene_factory

        self.leaderboard = Leaderboard()

        self.letters = [0, 0, 0]  # índices em ALPHABET -> começa em "AAA"
        self.selected_slot = 0

        self.title_font = pygame.font.SysFont("Courier New", 42, bold=True)
        self.letter_font = pygame.font.SysFont("Courier New", 90, bold=True)
        self.hint_font = pygame.font.SysFont("Courier New", 20, bold=True)

    # ------------------------------------------------------------------ #

    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_LEFT:
                self.selected_slot = (self.selected_slot - 1) % 3

            elif event.key == pygame.K_RIGHT:
                self.selected_slot = (self.selected_slot + 1) % 3

            elif event.key == pygame.K_UP:
                idx = self.selected_slot
                self.letters[idx] = (self.letters[idx] - 1) % len(ALPHABET)

            elif event.key == pygame.K_DOWN:
                idx = self.selected_slot
                self.letters[idx] = (self.letters[idx] + 1) % len(ALPHABET)

            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.confirm_name()

    def confirm_name(self):
        name = "".join(ALPHABET[i] for i in self.letters)

        self.leaderboard.add_entry(name, self.score)

        # Remove a si mesma da pilha e entra com a próxima cena no lugar
        self.scene_manager.pop()
        self.scene_manager.push(self.next_scene_factory())

    def update(self):
        pass

    # ------------------------------------------------------------------ #

    def render(self, screen):
        screen.fill((10, 10, 15))

        screen_width, screen_height = screen.get_size()

        title_surf = self.title_font.render(
            "NOVO RECORDE!", True, (255, 220, 120)
        )
        title_rect = title_surf.get_rect(center=(screen_width // 2, 120))
        screen.blit(title_surf, title_rect)

        score_surf = self.hint_font.render(
            f"Pontuacao: {self.score}", True, (220, 220, 220)
        )
        score_rect = score_surf.get_rect(center=(screen_width // 2, 175))
        screen.blit(score_surf, score_rect)

        letter_gap = 110
        start_x = screen_width // 2 - letter_gap

        for i, letter_index in enumerate(self.letters):
            letter = ALPHABET[letter_index]

            color = (255, 220, 120) if i == self.selected_slot else (
                200, 200, 200)

            letter_surf = self.letter_font.render(letter, True, color)
            letter_rect = letter_surf.get_rect(
                center=(start_x + i * letter_gap, screen_height // 2)
            )
            screen.blit(letter_surf, letter_rect)

            if i == self.selected_slot:
                underline_rect = pygame.Rect(0, 0, 60, 6)
                underline_rect.center = (
                    letter_rect.centerx,
                    letter_rect.bottom + 20
                )
                pygame.draw.rect(screen, (255, 220, 120), underline_rect)

        hint_surf = self.hint_font.render(
            "SETAS para escolher   ENTER para confirmar",
            True,
            (150, 150, 150)
        )
        hint_rect = hint_surf.get_rect(
            center=(screen_width // 2, screen_height - 80)
        )
        screen.blit(hint_surf, hint_rect)
