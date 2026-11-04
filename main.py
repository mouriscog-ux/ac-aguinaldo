from __future__ import annotations
from database import Database
from game import DIFFICULTIES, choose_questions, play, valid_nickname
from ranking import format_ranking


def save_with_retry(db: Database, result) -> None:
    while True:
        try:
            db.register_game(result)
            print('Resultado salvo com sucesso.')
            return
        except Exception:
            retry = input('Não foi possível salvar o resultado. Tentar novamente? (S/N): ').strip().upper()
            if retry != 'S':
                print('Resultado mantido nesta sessão. Não foi salvo no banco.')
                return


def start_game(db: Database) -> None:
    while True:
        try:
            nickname = valid_nickname(input('Informe seu apelido: '))
            break
        except ValueError as error:
            print(error)
    try:
        pools = {difficulty: db.get_questions(difficulty) for difficulty in DIFFICULTIES}
        questions = choose_questions(pools)
        game_id = db.get_or_create_game()
    except Exception as error:
        print(f'Não foi possível preparar a partida: {error}')
        return
    result = play(nickname, game_id, questions)
    print(f'\nFim da partida: {result.motivo_encerramento}; {result.acertos} acerto(s); R$ {result.valor_ganho:,.0f}; {result.tempo_segundos:.2f}s.'.replace(',', '.'))
    save_with_retry(db, result)


def main() -> None:
    try:
        db = Database()
    except RuntimeError as error:
        print(error)
        return
    while True:
        print('\n=== SHOW DO MILHÃO ===\n1. Iniciar jogo\n2. Ver ranking\n3. Sair')
        choice = input('Escolha: ').strip()
        if choice == '1': start_game(db)
        elif choice == '2':
            try: print(format_ranking(db.ranking()))
            except Exception as error: print(f'Não foi possível consultar o ranking: {error}')
        elif choice == '3': print('Até logo!'); return
        else: print('Opção inválida.')


if __name__ == '__main__':
    main()

