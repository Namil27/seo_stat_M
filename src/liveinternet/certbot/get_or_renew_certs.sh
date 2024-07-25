#!/bin/sh

# Запуск Nginx
nginx &

# Запуск Certbot
certbot --nginx --non-interactive --agree-tos --email namil05@yandex.ru -d stat.miliutin.ru

# Оставить контейнер в рабочем состоянии
tail -f /var/log/nginx/access.log
