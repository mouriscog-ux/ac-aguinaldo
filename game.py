"""Terminal game rules, independent of the database and user interface."""
from __future__ import annotations

import random
import time
import uuid
from collections.abc import Callable
from models import GameResult, Question

PRIZES = (1_000, 5_000, 10_000, 25_000, 50_000, 100_000, 200_000, 500_000, 1_000_000)
DIFFICULTIES = ('facil', 'media', 'dificil')


def choose_questions(questions_by_difficulty: dict[str, list[Question]], rng: random.Random | None = None) -> list[Question]:
    rng = rng or random.Random()
    selected: list[Question] = []
    for difficulty in DIFFICULTIES:
        pool = questions_by_difficulty.get(difficulty, [])
        if len(pool) < 3:
            raise ValueError(f'São necessárias ao menos 3 perguntas de dificuldade {difficulty}.')
        selected.extend(rng.sample(pool, 3))
    if len({q.id for q in selected}) != 9:
        raise ValueError('Há perguntas repetidas entre as dificuldades.')
    return selected


def valid_nickname(value: str) -> str:
    nickname = value.strip()
    if not nickname or len(nickname) > 40:
        raise ValueError('O apelido deve ter entre 1 e 40 caracteres.')
    return nickname


def play(nickname: str, game_id: str, questions: list[Question], ask: Callable[[str], str] = input,
         tell: Callable[[str], None] = print, clock: Callable[[], float] = time.perf_counter) -> GameResult:
    nickname = valid_nickname(nickname)
    if len(questions) != 9:
        raise ValueError('Uma partida deve ter exatamente 9 perguntas.')
    earned = 0
    hits = 0
    reason = 'concluiu'
    start = clock()
    for number, question in enumerate(questions, start=1):
        tell(f'\nPergunta {number} de 9 — vale R$ {PRIZES[number - 1]:,.0f}'.replace(',', '.'))
        tell(question.enunciado)
        for letter in 'ABCD':
            tell(f'{letter}) {question.alternativas[letter]}')
        while True:
            answer = ask('Resposta (A-D ou S para desistir): ').strip().upper()
            if answer in {'A', 'B', 'C', 'D', 'S'}:
                break
            tell('Entrada inválida. Digite A, B, C, D ou S.')
        if answer == 'S':
            reason = 'desistiu'
            break
        if answer != question.correta:
            reason = 'errou'
            tell(f'Resposta incorreta. A correta era {question.correta}.')
            break
        hits += 1
        earned = PRIZES[number - 1]
        tell(f'Resposta correta! Prêmio atual: R$ {earned:,.0f}'.replace(',', '.'))
    elapsed = max(0.0, clock() - start)
    if hits == 9:
        tell('Parabéns! Você ganhou R$ 1.000.000!')
    return GameResult(uuid.uuid4(), game_id, nickname, earned, elapsed, hits, reason)

