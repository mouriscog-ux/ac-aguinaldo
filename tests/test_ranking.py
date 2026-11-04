import unittest
from ranking import format_ranking

class RankingTests(unittest.TestCase):
    def test_empty_ranking(self): self.assertIn('não há', format_ranking([]))
    def test_display_has_position_and_data(self):
        text=format_ranking([{'apelido':'Ana','valor_ganho':1000,'tempo_segundos':1.25,'data_hora':'2026-01-02T12:00:00+00:00'}])
        self.assertIn('1',text);self.assertIn('Ana',text);self.assertIn('02/01/2026',text)

