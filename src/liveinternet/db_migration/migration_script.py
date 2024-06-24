from migration_funcs import *
from data_migration import *
from list_old_medias import table_list


def migration(connection_serv, connection_local):
    # Получаем список существующих таблиц в БД.
    old_tables_list = table_list
    # В данном случае полученные названия таблиц также являются доменными именами.
    for domain in old_tables_list:
        if domain in {"newia.ru", "news.vtomske.ru", "kurer-sreda.ru",  "sb.by"}:
            continue
        if domain in {"gazeta_all"}:
            domain = get_domain_name_by_uniq_id(connection_local, domain)
        # Получаем уникальный идентификатор по которому будет создаваться новая таблица.
        uniq_id = get_uniq_id_by_domain_name_sinx(connection_local, domain)
        # Создаем новую таблицу с названием по уникальному идентификатору.
        add_redaction_table(connection_serv, uniq_id)
        # Загружаем в новую таблицу старые данные.
        insert_data_into_timescaledb_from_file(connection_serv, domain=domain, uniq_id=uniq_id)
    # Все закрываем.
    connection_serv.close()
    connection_local.close()


if __name__ == "__main__":
    migration(connection_serv=connection_server, connection_local=connection_localhost)
