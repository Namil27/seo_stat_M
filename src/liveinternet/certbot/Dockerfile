# Используем образ certbot на основе Alpine Linux
FROM certbot/certbot:v2.6.0

# Устанавливаем crond
RUN apk update && apk add --no-cache cronie

# Копируем скрипт для обновления сертификатов
COPY renew_certificates.sh /usr/local/bin/renew_certificates.sh
RUN chmod +x /usr/local/bin/renew_certificates.sh

# Копируем кронтаб файл и создаем задание
COPY crontab /etc/crontabs/root

# Запуск crond
CMD ["crond", "-f"]
