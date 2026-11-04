from __future__ import annotations
from datetime import datetime


def format_ranking(rows: list[dict]) -> str:
    if not rows:
        return 'Ainda não há partidas registradas.'
    lines = ['POS  APELIDO                   PRÊMIO          TEMPO      DATA']
    for position, row in enumerate(rows, 1):
        date = datetime.fromisoformat(row['data_hora'].replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M')
        lines.append(f"{position:>2}   {row['apelido'][:24]:<24} R$ {int(row['valor_ganho']):>9,.0f}  {float(row['tempo_segundos']):>7.2f}s  {date}".replace(',', '.'))
    return '\n'.join(lines)

