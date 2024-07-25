#!/bin/sh

# Переменные
DOMAIN=stat.miliutin.ru
EMAIL=namil05@yandex.ru
WEBROOT=/var/www/certbot

# Создаем директорию webroot, если ее нет
mkdir -p $WEBROOT

# Получаем или обновляем сертификат
certbot certonly --webroot -w $WEBROOT --non-interactive --agree-tos --email $EMAIL -d $DOMAIN --keep-until-expiring --renew-with-new-domains

# Перезагружаем Nginx, чтобы применить новые сертификаты
nginx -s reload
