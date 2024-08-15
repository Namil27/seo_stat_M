#!/bin/bash

# Запись переменных окружения и задания cron в файл crontab
{
    echo "SHELL=/bin/bash"
    echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    env | grep -E 'DB_NAME|DB_USER|DB_HOST|DB_PORT|DB_PASSWORD|ACCESS_KEY|SECRET_KEY'
    echo "0 13 * * * /backup/backup.sh >> /var/log/cron.log 2>&1"
} > /etc/cron.d/backup-cron

# Установка прав и активация нового файла crontab
chmod 0644 /etc/cron.d/backup-cron
crontab /etc/cron.d/backup-cron

# Запуск cron в фоновом режиме
cron -f