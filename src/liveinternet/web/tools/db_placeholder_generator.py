from datetime import datetime, timedelta
import random

# Начало и конец марта 2024 года
start_date = datetime(2024, 6, 1)
end_date = datetime(2024, 6, 30)

# Генерация запросов для каждого дня в марте
sql_queries = []
current_date = start_date
while current_date <= end_date:
    formatted_date = current_date.strftime("%d.%m.%Y")
    random_guests = random.randint(15000, 30000)
    sql_queries.append(f"INSERT INTO data (date, guests) VALUES ('{formatted_date}', {random_guests});")
    current_date += timedelta(days=1)

# Объединяем запросы в один большой запрос с транзакцией
final_sql_query = "BEGIN TRANSACTION;\n" + "\n".join(sql_queries) + "\nCOMMIT;"

# Возвращаем первые и последние 3 строки запроса для проверки
sample_output = "\n".join(final_sql_query.split('\n')[:3]) + "\n...\n" + "\n".join(final_sql_query.split('\n')[-4:])
print(final_sql_query)
