import json
import os


class Leaderboard:
    """
    Ranking estilo arcade antigo: até MAX_ENTRIES posições, cada uma
    com um nome de exatamente 3 letras e uma pontuação.

    Começa vazio (sem ninguém no ranking) e persiste em disco (JSON),
    para sobreviver entre execuções do jogo — assim como nos arcades
    de verdade, o recorde continua lá da próxima vez que o fliperama
    for ligado.
    """

    MAX_ENTRIES = 10
    DEFAULT_PATH = os.path.join("data", "leaderboard.json")

    def __init__(self, path=None):
        self.path = path or self.DEFAULT_PATH
        self.entries = []  # lista de dicts: {"name": "AAA", "score": 1234}
        self.load()

    # ------------------------------------------------------------------ #
    #  Persistência                                                      #
    # ------------------------------------------------------------------ #

    def load(self):
        self.entries = []

        if not os.path.exists(self.path):
            return

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                for item in data:
                    name = str(item.get("name", "???"))[:3].upper()
                    score = int(item.get("score", 0))
                    self.entries.append({"name": name, "score": score})

            self._sort_and_trim()

        except (json.JSONDecodeError, OSError, ValueError, AttributeError, TypeError):
            # Arquivo corrompido ou em formato inesperado: começa vazio
            # em vez de derrubar o jogo.
            self.entries = []

    def save(self):
        try:
            directory = os.path.dirname(self.path)
            if directory:
                os.makedirs(directory, exist_ok=True)

            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.entries, f, ensure_ascii=False, indent=2)

        except OSError:
            # Se não der pra salvar (ex: sem permissão), o jogo segue
            # normalmente, só que sem persistir o ranking dessa vez.
            pass

    # ------------------------------------------------------------------ #
    #  Regras do ranking                                                 #
    # ------------------------------------------------------------------ #

    def _sort_and_trim(self):
        self.entries.sort(key=lambda e: e["score"], reverse=True)
        self.entries = self.entries[: self.MAX_ENTRIES]

    def qualifies(self, score):
        """
        True se essa pontuação entraria no top MAX_ENTRIES:
        sempre entra se o ranking ainda não está cheio, ou se for
        maior que o último colocado (10º) quando já estiver cheio.
        """
        if len(self.entries) < self.MAX_ENTRIES:
            return True
        return score > self.entries[-1]["score"]

    def add_entry(self, name, score):
        """Adiciona uma entrada, reordena, corta pro top 10 e salva."""
        name = (name or "???")[:3].upper().ljust(3, "?")

        self.entries.append({"name": name, "score": int(score)})
        self._sort_and_trim()
        self.save()

    def top_entries(self):
        """Cópia da lista de entradas, já ordenada do 1º ao último colocado."""
        return list(self.entries)
