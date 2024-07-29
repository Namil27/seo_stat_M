#!/bin/sh

# Запрашиваем сертификаты при запуске контейнера
certbot certonly --webroot -w /var/www/certbot -d stat.miliutin.ru --non-interactive --agree-tos --email namil05@yandex.ru

# Бесконечный цикл для обновления сертификатов каждую неделю
while true; do
  sleep 604800  # 604800 секунд = 1 неделя
  certbot renew --webroot -w /var/www/certbot
done
