# Используем официальный образ certbot
FROM certbot/certbot:latest

# Устанавливаем dcron
RUN apk add --no-cache --update dcron

# Создаем директорию для хранения сертификатов
RUN mkdir -p /etc/letsencrypt

# Копируем скрипт для получения и обновления сертификатов в контейнер
COPY get_or_renew_certs.sh /usr/bin/get_or_renew_certs.sh

# Копируем crontab файл
COPY crontab /etc/cron.d/certbot-cron

# Даем права на выполнение скрипта и crontab файла
RUN chmod +x /usr/bin/get_or_renew_certs.sh
RUN chmod 0644 /etc/cron.d/certbot-cron

# Создаем log файл для cron
RUN touch /var/log/cron.log

# Добавляем crontab в cron
RUN crontab /etc/cron.d/certbot-cron

# Получаем сертификат при первом запуске контейнера
RUN /usr/bin/get_or_renew_certs.sh

# Запускаем cron и tail для отображения логов
CMD crond -f -d 8 && tail -f /var/log/cron.log
