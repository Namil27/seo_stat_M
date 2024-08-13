#!/bin/bash

# Настройки
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_HOST=${DB_HOST}
DB_PORT=${DB_PORT}
DB_PASSWORD=${DB_PASSWORD}
BACKUP_DIR="/backup-data"
DATE=$(date +\%Y-\%m-\%d)
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}-${DATE}.backup"
REMOTE_STORAGE="selectel:liveinternet-backups"
RETENTION_DAYS=36

# Настройка rclone конфигурации через переменные окружения
mkdir -p /root/.config/rclone
cat <<EOF > /root/.config/rclone/rclone.conf
[selectel]
type = s3
provider = Other
env_auth = false
access_key_id = ${ACCESS_KEY}
secret_access_key = ${SECRET_KEY}
endpoint = s3.storage.selcloud.ru
EOF

# Создание бэкапа
PGPASSWORD=$DB_PASSWORD pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -F c -b -v -f $BACKUP_FILE $DB_NAME

# Проверка успешности создания бэкапа
if [ $? -ne 0 ]; then
  echo "Error: Backup creation failed."
  exit 1
fi

# Загрузка в Object Storage
rclone copy $BACKUP_FILE $REMOTE_STORAGE

# Проверка успешности загрузки
if [ $? -ne 0 ]; then
  echo "Error: Failed to upload backup to remote storage."
  exit 1
fi

# Удаление старых локальных бэкапов (старше 36 дней)
find $BACKUP_DIR -type f -name "*.backup" -mtime +$RETENTION_DAYS -exec rm {} \;

# Удаление старых бэкапов в Object Storage (старше 36 дней)
rclone delete --min-age ${RETENTION_DAYS}d $REMOTE_STORAGE