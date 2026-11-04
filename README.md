# Show do Milhão

Jogo de perguntas para terminal em Python, com partidas armazenadas no Supabase e um site independente, somente leitura, para o ranking.

## Componentes

- `main.py`, `game.py`: jogo no terminal, 9 perguntas (3 fáceis, 3 médias e 3 difíceis) e premiação até R$ 1 milhão.
- `database.py`: integração de servidor com Supabase. A chave nunca é colocada no site.
- `sql/schema.sql` e `sql/seguranca.sql`: esquema e regras de segurança do banco.
- `site/`: ranking responsivo para GitHub Pages.
- `tests/`: testes sem depender da rede.

## Instalação no Windows/VS Code

1. Abra esta pasta no VS Code e instale Python 3.11 ou superior.
2. No terminal integrado, execute:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Copie `.env.example` para `.env`. Informe `SUPABASE_URL` e `SUPABASE_KEY` no arquivo local. Use a chave de servidor somente para o jogo e nunca faça commit do `.env`.
4. No Supabase SQL Editor, confira a estrutura existente e execute `sql/schema.sql`, `sql/seguranca.sql` e `sql/jogo_web_seguro.sql`, nessa ordem. Revise os nomes reais das colunas antes de aplicar; os scripts não apagam perguntas nem partidas.
5. Execute `sql/perguntas.sql` uma vez em um banco vazio para inserir as 15 perguntas iniciais (cinco por dificuldade), ou mantenha o conjunto já cadastrado. Depois permita que o aplicativo crie o jogo `Show do Milhão` na primeira partida.
6. Valide e rode:

```bash
python test_connection.py
python -m unittest discover -s tests -v
python main.py
```

## Regras

O jogador informa um apelido, responde a nove perguntas em ordem de dificuldade e pode desistir antes de responder. O prêmio é o último nível alcançado (não uma soma). O cronômetro inicia na primeira pergunta e usa `time.perf_counter()`. Em falhas de gravação, a partida permanece em memória e o mesmo UUID é reutilizado ao tentar salvar novamente.

O ranking seleciona a melhor partida de cada apelido por jogo, desempata por prêmio, menor tempo, data mais antiga e UUID, e mostra os dez primeiros.

## Ranking web e GitHub Pages

Após aplicar o SQL, copie `site/config.js.example` para `site/config.js` e preencha apenas `anonKey` com a chave **anon pública** do Supabase. Não use a chave `service_role`/secreta. A view pública expõe somente dados de ranking; perguntas e partidas brutas não têm acesso anônimo.

No GitHub, envie o código sem `.env` e sem `site/config.js` se preferir manter sua chave fora do repositório (a chave anon é publicável, mas pode ser criada em ambiente de deploy). Em **Settings → Pages**, escolha **Deploy from a branch**, a branch desejada e a pasta `/site` (ou publique o conteúdo de `site` na raiz da branch de Pages). Confirme que `config.js` existe no artefato publicado. Os caminhos do site são relativos e funcionam em subdiretórios do GitHub Pages.

## Segurança e pendências de configuração

O repositório não contém `.env`; crie-o localmente a partir de `.env.example` e use `SUPABASE_SECRET_KEY` somente no Python. O site usa apenas a chave pública de `site/config.js`. Nunca exponha uma chave secreta. Caso uma chave secreta tenha sido publicada antes, rotacione-a no painel do Supabase.

As fontes do conjunto inicial estão em `fontes_perguntas.md`. A execução das migrações, o teste de conexão real e a validação da publicação dependem de credenciais e acesso ao projeto Supabase; ainda precisam ser confirmados no ambiente configurado.
