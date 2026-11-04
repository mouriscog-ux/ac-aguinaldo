import unittest
import uuid
from database import Database
from models import GameResult


class Query:
    def __init__(self): self.rows=[]; self.upserts=[]; self.orders=[]; self.filters=[]; self.limits=[]
    def upsert(self,row,**kwargs): self.upserts.append((row,kwargs)); return self
    def select(self,*args): return self
    def eq(self,*args): self.filters.append(args); return self
    def order(self,*args,**kwargs): self.orders.append((args,kwargs)); return self
    def limit(self,*args): self.limits.append(args); return self
    def execute(self): return type('Response',(),{'data':self.rows})()

class Client:
    def __init__(self): self.query=Query()
    def table(self, name): self.name=name; return self.query

class DatabaseTests(unittest.TestCase):
    def test_registration_reuses_partida_id_on_retry(self):
        c=Client(); db=Database(c); result=GameResult(uuid.uuid4(),'game','Ana',1000,2.2,1,'errou')
        db.register_game(result); db.register_game(result)
        self.assertEqual(len(c.query.upserts),2)
        self.assertEqual(c.query.upserts[0][0]['id'],c.query.upserts[1][0]['id'])
        self.assertEqual(c.query.upserts[0][1]['on_conflict'],'id')

    def test_ranking_uses_view_positions_without_global_limit(self):
        c=Client(); c.query.rows=[{'partida_id':'match-1','posicao':1}]; db=Database(c)
        self.assertEqual(db.ranking(), c.query.rows)
        self.assertEqual(c.query.orders, [(('posicao',), {})])
        self.assertEqual(c.query.limits, [])

    def test_ranking_can_filter_by_game(self):
        c=Client(); db=Database(c)
        db.ranking('game-1')
        self.assertEqual(c.query.filters, [('jogo_id','game-1')])

