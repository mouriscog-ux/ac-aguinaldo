-- Execute no SQL Editor do Supabase depois de schema.sql e seguranca.sql.
-- Não altera perguntas, jogos ou partidas existentes.
create table if not exists public.sessoes_jogo_web (
  id uuid primary key default gen_random_uuid(),
  jogo_id uuid not null references public.jogos(id),
  apelido varchar(40) not null check (length(trim(apelido)) > 0),
  perguntas jsonb not null,
  indice smallint not null default 0 check (indice between 0 and 9),
  acertos smallint not null default 0 check (acertos between 0 and 9),
  valor_ganho integer not null default 0,
  iniciada_em timestamptz not null default now(),
  finalizada_em timestamptz,
  motivo_encerramento text check (motivo_encerramento in ('errou', 'desistiu', 'concluiu'))
);

alter table public.sessoes_jogo_web enable row level security;
revoke all on public.sessoes_jogo_web from anon;

create or replace function public.iniciar_jogo_web(p_apelido text, p_jogo_id uuid)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_id uuid; v_questions jsonb; v_count integer;
begin
  if length(trim(coalesce(p_apelido, ''))) = 0 or length(trim(p_apelido)) > 40 then
    raise exception 'Apelido deve ter entre 1 e 40 caracteres.';
  end if;
  if not exists (select 1 from jogos where id = p_jogo_id) then
    raise exception 'Jogo não encontrado.';
  end if;
  with sorteadas as (
    select id, enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, dificuldade,
      row_number() over (partition by dificuldade order by random()) as ordem
    from perguntas where dificuldade in ('facil', 'media', 'dificil')
  ), selecionadas as (
    select * from sorteadas where ordem <= 3
  )
  select count(*), jsonb_agg(jsonb_build_object(
    'id', id, 'enunciado', enunciado, 'alternativa_a', alternativa_a,
    'alternativa_b', alternativa_b, 'alternativa_c', alternativa_c,
    'alternativa_d', alternativa_d, 'dificuldade', dificuldade
  ) order by case dificuldade when 'facil' then 1 when 'media' then 2 else 3 end, ordem)
  into v_count, v_questions from selecionadas;
  if v_count <> 9 then
    raise exception 'O banco precisa ter ao menos 3 perguntas fáceis, 3 médias e 3 difíceis.';
  end if;
  insert into sessoes_jogo_web (jogo_id, apelido, perguntas)
  values (p_jogo_id, trim(p_apelido), v_questions) returning id into v_id;
  return jsonb_build_object('sessao_id', v_id, 'perguntas', v_questions);
end;
$$;

create or replace function public.responder_jogo_web(p_sessao_id uuid, p_pergunta_id uuid, p_resposta text, p_desistir boolean default false)
returns jsonb language plpgsql security definer set search_path = public, pg_temp as $$
declare
  s sessoes_jogo_web%rowtype; v_esperada uuid; v_correta text; v_acertos smallint;
  v_valor integer; v_motivo text; v_tempo numeric(12,3); v_encerrada boolean := false;
  v_premios integer[] := array[1000,5000,10000,25000,50000,100000,200000,500000,1000000];
begin
  select * into s from sessoes_jogo_web where id = p_sessao_id for update;
  if not found then raise exception 'Sessão não encontrada.'; end if;
  if s.finalizada_em is not null then raise exception 'Esta partida já foi encerrada.'; end if;
  v_esperada := (s.perguntas -> s.indice ->> 'id')::uuid;
  if v_esperada <> p_pergunta_id then raise exception 'Pergunta inválida para esta sessão.'; end if;
  v_tempo := round(extract(epoch from now() - s.iniciada_em)::numeric, 3);
  if p_desistir then
    v_motivo := 'desistiu'; v_valor := s.valor_ganho; v_acertos := s.acertos; v_encerrada := true;
  else
    if upper(coalesce(p_resposta, '')) not in ('A','B','C','D') then raise exception 'Resposta inválida.'; end if;
    select correta into v_correta from perguntas where id = v_esperada;
    if upper(p_resposta) = v_correta then
      v_acertos := s.acertos + 1; v_valor := v_premios[v_acertos];
      if v_acertos = 9 then v_motivo := 'concluiu'; v_encerrada := true; end if;
    else
      v_acertos := s.acertos; v_valor := s.valor_ganho; v_motivo := 'errou'; v_encerrada := true;
    end if;
  end if;
  if v_encerrada then
    update sessoes_jogo_web set acertos=v_acertos, valor_ganho=v_valor, finalizada_em=now(), motivo_encerramento=v_motivo where id=s.id;
    insert into partidas (id, jogo_id, apelido, valor_ganho, tempo_segundos, acertos, motivo_encerramento)
    values (s.id, s.jogo_id, s.apelido, v_valor, v_tempo, v_acertos,
      case v_motivo when 'errou' then 'erro' when 'desistiu' then 'desistencia' when 'concluiu' then 'completo' end)
    on conflict (id) do nothing;
  else
    update sessoes_jogo_web set indice=indice+1, acertos=v_acertos, valor_ganho=v_valor where id=s.id;
  end if;
  return jsonb_build_object('encerrada', v_encerrada, 'motivo', v_motivo, 'acertos', v_acertos,
    'valor_ganho', v_valor, 'tempo_segundos', v_tempo, 'correta', v_correta);
end;
$$;

revoke all on function public.iniciar_jogo_web(text, uuid) from public;
revoke all on function public.responder_jogo_web(uuid, uuid, text, boolean) from public;
grant execute on function public.iniciar_jogo_web(text, uuid) to anon;
grant execute on function public.responder_jogo_web(uuid, uuid, text, boolean) to anon;
