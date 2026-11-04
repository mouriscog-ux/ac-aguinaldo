-- Execute once in Supabase SQL Editor. It creates objects only when absent.
create extension if not exists pgcrypto;

create table if not exists public.jogos (
  id uuid primary key default gen_random_uuid(),
  nome text not null unique,
  created_at timestamptz not null default now()
);

create table if not exists public.perguntas (
  id uuid primary key default gen_random_uuid(),
  enunciado text not null,
  alternativa_a text not null, alternativa_b text not null,
  alternativa_c text not null, alternativa_d text not null,
  correta char(1) not null check (correta in ('A','B','C','D')),
  dificuldade text not null check (dificuldade in ('facil','media','dificil'))
);

create table if not exists public.partidas (
  id uuid primary key,
  jogo_id uuid not null references public.jogos(id),
  apelido varchar(40) not null check (length(trim(apelido)) > 0),
  valor_ganho integer not null check (valor_ganho in (0,1000,5000,10000,25000,50000,100000,200000,500000,1000000)),
  tempo_segundos numeric(12,3) not null check (tempo_segundos >= 0),
  acertos smallint not null check (acertos between 0 and 9),
  motivo_encerramento text not null check (motivo_encerramento in ('errou','desistiu','concluiu')),
  data_hora timestamptz not null default now()
);

create index if not exists partidas_ranking_idx on public.partidas (jogo_id, valor_ganho desc, tempo_segundos asc, data_hora asc, id asc);

