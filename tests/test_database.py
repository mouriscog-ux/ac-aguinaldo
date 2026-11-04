import unittest
import uuid
from database import Database
from models import GameResult


class Query:
    def __init__(self): self.rows=[]; self.upserts=[]
    def upsert(self,row,**kwargs): self.upserts.append((row,kwargs)); return self
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

