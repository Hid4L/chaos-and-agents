from dataclasses import dataclass

@dataclass
class Config:
    system: str
    seed: int | None = None

    # parámetros genéricos
    points: int = 10000
    dt: float = 0.01

    # específicos (opcionales)
    a: float = 1.4
    b: float = 0.3
    c: float = 5.7