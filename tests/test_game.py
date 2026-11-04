import random
import unittest
from game import PRIZES, choose_questions, play, valid_nickname
from models import Question


def q(i, difficulty='facil', correct='A'):
    return Question(str(i), f'Pergunta {i}', {'A':'a','B':'b','C':'c','D':'d'}, correct, difficulty)


class GameTests(unittest.TestCase):
    def test_selects_three_per_level_without_repetition(self):
        pools = {d:[q(f'{d}{i}', d) for i in range(5)] for d in ('facil','media','dificil')}
        selected = choose_questions(pools, random.Random(3))
        self.assertEqual([x.dificuldade for x in selected], ['facil']*3+['media']*3+['dificil']*3)
        self.assertEqual(len({x.id for x in selected}), 9)

    def test_all_correct_wins_million_and_measures_time(self):
        ticks = iter([10, 25.5]); result = play('Ana','g',[q(i) for i in range(9)], ask=lambda _: 'A', tell=lambda _:None, clock=lambda:next(ticks))
        self.assertEqual((result.acertos,result.valor_ganho,result.motivo_encerramento,result.tempo_segundos),(9,1_000_000,'concluiu',15.5))

    def test_first_error_and_invalid_answer(self):
        answers=iter(['x','B']); messages=[]; result=play('Ana','g',[q(i) for i in range(9)],ask=lambda _:next(answers),tell=messages.append,clock=lambda:0)
        self.assertEqual((result.acertos,result.valor_ganho,result.motivo_encerramento),(0,0,'errou'))
        self.assertTrue(any('inválida' in x for x in messages))

    def test_error_after_hits_and_quit(self):
        answers=iter(['A','A','S']);result=play('Ana','g',[q(i) for i in range(9)],ask=lambda _:next(answers),tell=lambda _:None,clock=lambda:0)
        self.assertEqual((result.acertos,result.valor_ganho,result.motivo_encerramento),(2,PRIZES[1],'desistiu'))

    def test_nickname_validation(self):
        with self.assertRaises(ValueError): valid_nickname('  ')
        self.assertEqual(valid_nickname(' Ana '), 'Ana')

