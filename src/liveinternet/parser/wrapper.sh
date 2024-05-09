#!/bin/bash
# Установка переменных окружения
export DB_HOST="timescaledb"
export DB_PORT="5432"
export DB_USER="api"
export DB_PASSWORD="super_hard_password"
export DB_NAME="liveinternet"

# Запуск Python скрипта
/usr/local/bin/python3 /app/parser.py >> /var/log/cron.log 2>&1
