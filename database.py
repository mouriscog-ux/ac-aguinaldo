"""Small, server-side-only gateway for the Supabase tables."""
from __future__ import annotations

from typing import Any
from supabase import create_client
from config import supabase_settings
from models import GameResult, Question


class Database:
    def __init__(self, client: Any | None = None) -> None:
        if client is None:
            url, key = supabase_settings()
            client = create_client(url, key)
        self.client = client

    def test_connection(self) -> bool:
        self.client.table('jogos').select('id').limit(1).execute()
        return True

    def get_questions(self, difficulty: str) -> list[Question]:
        response = (self.client.table('perguntas').select(
            'id,enunciado,alternativa_a,alternativa_b,alternativa_c,alternativa_d,correta,dificuldade'
        ).eq('dificuldade', difficulty).execute())
        return [Question(
            id=str(row['id']), enunciado=row['enunciado'],
            alternativas={'A': row['alternativa_a'], 'B': row['alternativa_b'],
                          'C': row['alternativa_c'], 'D': row['alternativa_d']},
            correta=str(row['correta']).upper(), dificuldade=row['dificuldade']
        ) for row in response.data]

    def get_or_create_game(self, name: str = 'Show do Milhão') -> str:
        found = self.client.table('jogos').select('id').eq('nome', name).limit(1).execute().data
        if found:
            return str(found[0]['id'])
        return str(self.client.table('jogos').insert({'nome': name}).execute().data[0]['id'])

    def register_game(self, result: GameResult) -> None:
        # The client-generated UUID and a unique primary key make retries idempotent.
        row = {'id': str(result.id), 'jogo_id': result.jogo_id, 'apelido': result.apelido,
               'valor_ganho': result.valor_ganho, 'tempo_segundos': round(result.tempo_segundos, 3),
               'acertos': result.acertos, 'motivo_encerramento': result.motivo_encerramento}
        self.client.table('partidas').upsert(row, on_conflict='id').execute()

    def ranking(self, game_id: str | None = None) -> list[dict[str, Any]]:
        query = self.client.table('ranking_publico').select('*')
        if game_id:
            query = query.eq('jogo_id', game_id)
        return query.order('valor_ganho', desc=True).order('tempo_segundos').order('data_hora').order('partida_id').limit(10).execute().data

