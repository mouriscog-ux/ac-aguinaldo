# Registro de uso de IA

## 4 de novembro de 2026 — Codex (GPT-5)

- **Objetivo:** implementar a aplicação terminal, integração segura com Supabase, ranking web, SQL, testes e documentação do projeto Show do Milhão.
- **Prompt completo:** “adicione tudo nessa pasta”, acompanhado do briefing “PROJETO COMPLETO — SHOW DO MILHÃO”.
- **Como a resposta foi utilizada:** foram criados os arquivos da aplicação e da documentação nesta pasta vazia. Não há histórico de prompts anteriores disponível neste repositório; ele deve ser complementado pelo autor caso exista.
- **Alterações realizadas:** regras de partida e premiação, acesso ao Supabase por variáveis de ambiente, migrações SQL, site somente-leitura, testes unitários e README.
- **Arquivos/funções afetados:** `game.py` (`choose_questions`, `play`), `database.py`, `main.py`, `sql/*.sql`, `site/*`, `tests/*`.
- **Problema/correção/teste:** o ranking não deve consultar a tabela `partidas` diretamente, pois ela contém mais dados do que o site precisa. Foi criada a view `ranking_publico` e removido o acesso `anon` à tabela. A consulta é verificada pela configuração em `sql/seguranca.sql`; após executar a migração, validar no navegador e com o teste de integração descrito no README.
- **Testes executados:** registrar aqui o resultado do comando `python -m unittest discover -s tests` executado no ambiente do projeto.

