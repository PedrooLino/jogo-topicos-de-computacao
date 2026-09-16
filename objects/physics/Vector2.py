import math


class Vector2:
    __slots__ = ("x", "y")

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    # ---------------- Operadores ----------------
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __eq__(self, other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __iter__(self):
        # permite fazer `x, y = vetor` quando um pygame.Rect/blit pedir uma tupla
        yield self.x
        yield self.y

    def __repr__(self):
        return f"Vector2({self.x:.2f}, {self.y:.2f})"

    # ---------------- Geometria ----------------
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalized(self):
        l = self.length()
        if l == 0:
            return Vector2(0, 0)
        return Vector2(self.x / l, self.y / l)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def angle(self):
        """Ângulo do vetor em radianos (atan2(y, x))."""
        return math.atan2(self.y, self.x)

    def rotated(self, angle_rad):
        """Retorna uma cópia deste vetor rotacionada por angle_rad radianos."""
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a,
        )

    @staticmethod
    def from_angle(angle_rad, length=1.0):
        return Vector2(math.cos(angle_rad) * length, math.sin(angle_rad) * length)

    def copy(self):
        return Vector2(self.x, self.y)
