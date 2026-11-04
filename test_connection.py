from database import Database

if __name__ == '__main__':
    try:
        Database().test_connection()
        print('Conexão com Supabase confirmada.')
    except Exception as error:
        print(f'Falha na conexão: {error}')
        raise SystemExit(1)
