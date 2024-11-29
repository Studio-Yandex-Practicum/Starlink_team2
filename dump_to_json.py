import psycopg2
import json

tables = ('roles', 'menus', 'employee_emails', 'telegramusers')

conn = psycopg2.connect(
    dbname="postgres",
    user="user",
    password="pass",
    host="localhost",
    port=5432
)

for table in tables:
    # Создаем курсор
    cur = conn.cursor()

    # SQL-запрос для извлечения данных из таблицы
    query = f"SELECT * FROM {table};"
    cur.execute(query)

    # Извлекаем данные
    rows = cur.fetchall()

    # Получаем имена колонок
    columns = [desc[0] for desc in cur.description]

    # Формируем список словарей (каждая строка - словарь)
    data = [dict(zip(columns, row)) for row in rows]

    # Сохраняем данные в JSON
    with open(f'data/{table}.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    # Закрываем соединение
    cur.close()

    print(f"Данные успешно сохранены в {table}.json")

conn.close()
