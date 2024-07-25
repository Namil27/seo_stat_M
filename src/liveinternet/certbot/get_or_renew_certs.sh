#!/bin/sh

# Переменные для домена и email
DOMAIN=stat.miliutin.ru
EMAIL=namil05@yandex.ru
WEBROOT=/var/www/certbot

# Создаем директорию для webroot, если ее нет
mkdir -p $WEBROOT

# Запуск certbot для получения или обновления сертификатов
certbot certonly --webroot -w $WEBROOT --non-interactive --agree-tos --email $EMAIL -d $DOMAIN --keep-until-expiring --renew-with-new-domains
