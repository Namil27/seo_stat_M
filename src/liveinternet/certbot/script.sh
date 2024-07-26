#!/bin/sh

# Получаем сертификат
certbot certonly --webroot -w /var/www/certbot -d stat.miliutin.ru --non-interactive --agree-tos --email namil05@yandex.ru

# Дополнительные команды, если нужно