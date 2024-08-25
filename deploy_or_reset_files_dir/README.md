Гайд на деплой проекта на сервере(убунту):
    1) На сервере должен быть установлен crontab, docker и docker-compose. 
    2) В папке /home создаем папку с проектом (stat_mil_ru), внутри этого проекта создаем папку project.
    3) В папку /home/stat_mil_ru/ копируем файл deploy.sh из проекта с удаленного репозитория 
        (/deploy_or_reset_files_dir/deploy.sh).
    4) Создаем папку в корне с названием ssl, в ней папку ssl_stat, в ней 2 папки conf и www.
        в папке conf создаем папку .well-known в ней acme-challenge .
    5) Прописываем bash deploy.sh и все устанавливается.
    6) После установки прописываем команду "crontab -e" и в открывшемся текстовом редакторе прописываем
        "@monthly cd /home/stat_mil_ru/project/src/liveinternet && docker-compose restart certbot"