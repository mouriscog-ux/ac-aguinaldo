-- Run after schema.sql. Server-side game uses SUPABASE_KEY; the site receives only SUPABASE_ANON_KEY.
alter table public.jogos enable row level security;
alter table public.perguntas enable row level security;
alter table public.partidas enable row level security;

-- Do not grant anonymous users access to questions or raw matches.
revoke all on public.perguntas, public.partidas from anon;
grant select on public.jogos to anon;
create policy "anon may read game names" on public.jogos for select to anon using (true);

-- One best row per nickname and game, then top 10 per game.
-- The owner-owned view exposes only its projected columns; anonymous roles have
-- no privilege on the underlying tables. Keep this view owned by postgres.
create or replace view public.ranking_publico
with (security_barrier = true) as
with melhores as (
  select p.id as partida_id, p.jogo_id, p.apelido, p.valor_ganho, p.tempo_segundos, p.data_hora,
         row_number() over (partition by p.jogo_id, lower(p.apelido)
           order by p.valor_ganho desc, p.tempo_segundos asc, p.data_hora asc, p.id asc) as melhor
  from public.partidas p
), classificados as (
  select *, row_number() over (partition by jogo_id
    order by valor_ganho desc, tempo_segundos asc, data_hora asc, partida_id asc) as posicao
  from melhores where melhor = 1
)
select partida_id, jogo_id, apelido, valor_ganho, tempo_segundos, data_hora, posicao
from classificados where posicao <= 10;

grant select on public.ranking_publico to anon;
-- The view is intentionally the only public source of ranking data.

