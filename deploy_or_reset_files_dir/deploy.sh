#!/bin/bash

#Удаляем папку с проектом
rm -rf /home/stat_mil_ru/project

# Создаем директорию, если ее нет
mkdir -p /home/stat_mil_ru/project

# Клонируем репозиторий
git clone --branch back https://namil27:aae7ab67-f804-4616-a2bb-4b692ad5126c@gi>


# Переходим в директорию с проектом
cd /home/stat_mil_ru/project/src/liveinternet/certbot/

mkdir conf

mkdir -p www/.well-known/acme-challenge

cd ../
# Строим и запускаем контейнеры
docker-compose build --no-cache && docker-compose up -d

# Удалям файл с настройкой для получения ключей
rm nginx/nginx.conf

# Перемещаемся в nginx
cd nginx

# Меняем название файла с настройкой https тем самым делая его новым конфигом nginx
mv nginx_https.conf nginx.conf

# Удаляем ненужные образы
docker image prune -a -f
