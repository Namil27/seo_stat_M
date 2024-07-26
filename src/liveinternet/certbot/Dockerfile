# Используем официальный образ Certbot
FROM certbot/certbot:v2.6.0

# Устанавливаем cron (crond) и необходимые утилиты
RUN apk add --no-cache dcron

RUN mkdir app
# Копируем скрипт и файл с задачей cron в контейнер
COPY script.sh /app/script.sh
COPY crontab /etc/crontabs/root

# Делаем скрипт исполняемым
RUN chmod +x /app/script.sh

# Запускаем crond в форева режиме
CMD ["sh", "crontab", "-f"]
