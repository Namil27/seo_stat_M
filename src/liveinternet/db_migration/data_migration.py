import psycopg2

# Данные для подключения к базе данных
db_name = "liveinternet"  # имя базы данных
db_user = "postgres"  # имя пользователя
db_password = f"i@eS*gs@4fSwBg\\"  # пароль пользователя
db_host = "23.111.123.4"  # хост, если база данных находится на той же машине
db_port = "5432"  # порт PostgreSQL по умолчанию

db_name1 = "liveinternet"
db_password1 = ""  # пароль пользователя
db_host1 = "localhost"  # хост, если база данных находится на той же машине

connection_server = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)

connection_localhost = psycopg2.connect(
    dbname=db_name1,
    user=db_user,
    password=db_password1,
    host=db_host1,
    port=db_port
)
