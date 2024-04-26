import datetime
from full_cycle_funcs import *


def full_cycle():
    """
    Функция собирающая данные и записывающая их в БД.
    """
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    # Сохраняем данные в today
    today_media_reit = pars_reit_today(1, 4)

    for media in today_media_reit:
        add_redaction_table(media[0])
        add_data_in_table(media[0], date, media[1])


full_cycle()
