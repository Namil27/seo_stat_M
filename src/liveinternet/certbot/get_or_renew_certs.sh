#!/bin/bash

# Переменные для домена и email
DOMAIN=stat.miliutin.ru
EMAIL=namil05@yandex.ru

# Запуск certbot для получения или обновления сертификатов
certbot certonly --standalone --non-interactive --agree-tos --email $EMAIL -d $DOMAIN --keep-until-expiring --renew-with-new-domains

# Если сертификаты успешно получены или обновлены, они будут находиться в /etc/letsencrypt/live/$DOMAIN/
# Добавьте здесь любые дополнительные команды, если необходимо
