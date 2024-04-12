import psycopg2

try:
    db = psycopg2.connect(host='127.0.0.1',
                        port=5432,
                        user='postgres',
                        password='password')
    cur = db.cursor()
    print("Подключение к БД прошло успешно.")
except Exception as e:
    db = None
    print(f"Не удалось подключиться к БД. {e}")