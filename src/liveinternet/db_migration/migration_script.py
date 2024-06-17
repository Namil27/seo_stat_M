from migration_funcs import *
from data_migration import *


def migration(connection_serv, connection_local):
    # Получаем список существующих таблиц в БД.
    old_tables_list = take_old_tables(connection_serv)
    # В данном случае полученные названия таблиц также являются доменными именами.
    for domain in old_tables_list:
        # Получаем уникальный идентификатор по которому будет создаваться новая таблица.
        uniq_id = get_uniq_id_by_domain_name_sinx(connection_local, domain)
        # Сохраняем данные из таблицы в файл json.
        save_data_as_json(connection_serv, domain)
        # Создаем новую таблицу с названием по уникальному идентификатору.
        add_redaction_table(connection_serv, uniq_id)
        # Загружаем в новую таблицу старые данные.
        insert_data_into_timescaledb_from_file(connection_serv, domain=domain, uniq_id=uniq_id)
        # Удаляем старые таблицы.
        delete_table(connection_serv, domain)

    # Все закрываем.
    connection_serv.close()
    connection_local.close()


if __name__ == "__main__":
    migration(connection_serv=connection_server, connection_local=connection_localhost)
