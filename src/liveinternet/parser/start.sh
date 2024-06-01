#!/bin/bash
# Запись переменных окружения и дополнительных строк в файл crontab
{
    echo "SHELL=/bin/bash"
    echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    env
    echo "55 20 * * * /usr/local/bin/python3 /app/parser.py >> /var/log/cron.log 2>&1" # задача cron
} > /etc/cron.d/parser-cron

# Установка прав и активация нового файла crontab
chmod 0644 /etc/cron.d/parser-cron
crontab /etc/cron.d/parser-cron

# Запуск cron в фоновом режиме
cron -f
