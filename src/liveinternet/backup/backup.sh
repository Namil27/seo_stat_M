#!/bin/bash

# Настройки
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_HOST=${DB_HOST}
DB_PORT=${DB_PORT}
BACKUP_DIR="/backup"
DATE=$(date +\%Y-\%m-\%d)
BACKUP_FILE="$BACKUP_DIR/$DB_NAME-$DATE.sql"
REMOTE_STORAGE="selectel:liveinternet-backups"
RETENTION_DAYS=36

# Настройка rclone конфигурации через переменные окружения
export RCLONE_CONFIG_SELECTEL_TYPE=s3
export RCLONE_CONFIG_SELECTEL_PROVIDER=Selectel
export RCLONE_CONFIG_SELECTEL_ENV_AUTH=false
export RCLONE_CONFIG_SELECTEL_ACCESS_KEY_ID=$ACCESS_KEY
export RCLONE_CONFIG_SELECTEL_SECRET_ACCESS_KEY=$SECRET_KEY
export RCLONE_CONFIG_SELECTEL_ENDPOINT=s3.storage.selcloud.ru

# Создание бэкапа
pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME > $BACKUP_FILE

# Загрузка в Object Storage
rclone copy $BACKUP_FILE $REMOTE_STORAGE

# Удаление старых локальных бэкапов (старше 36 дней)
find $BACKUP_DIR -type f -name "*.sql" -mtime +$RETENTION_DAYS -exec rm {} \;

# Удаление старых бэкапов в Object Storage (старше 36 дней)
rclone delete --min-age ${RETENTION_DAYS}d $REMOTE_STORAGE