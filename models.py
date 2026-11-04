from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Question:
    id: str
    enunciado: str
    alternativas: dict[str, str]
    correta: str
    dificuldade: str


@dataclass(frozen=True)
class GameResult:
    id: UUID
    jogo_id: str
    apelido: str
    valor_ganho: int
    tempo_segundos: float
    acertos: int
    motivo_encerramento: str

