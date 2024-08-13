#!/bin/bash

# Функция для отображения помощи
usage() {
  echo "Usage: $0 -d <backup_date>"
  exit 1
}

# Обработка параметров
while getopts ":d:" opt; do
  case ${opt} in
    d )
      BACKUP_DATE=$OPTARG
      ;;
    \? )
      usage
      ;;
  esac
done
shift $((OPTIND -1))

# Проверка, что дата бэкапа передана как аргумент
if [ -z "$BACKUP_DATE" ]; then
  echo "Error: Backup date is required."
  usage
fi

# Проверка переменных окружения
if [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ] || [ -z "$DB_PASSWORD" ] || [ -z "$ACCESS_KEY" ] || [ -z "$SECRET_KEY" ]; then
  echo "Error: One or more environment variables are missing."
  exit 1
fi

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

# Формирование имени файла бэкапа
REMOTE_BACKUP_FILE="liveinternet-backups/${DB_NAME}-${BACKUP_DATE}.backup"

# Локальный файл для восстановления
LOCAL_BACKUP_FILE="/backup/restore-data/${DB_NAME}-${BACKUP_DATE}.backup"

# Создание директории для локального файла, если она не существует
mkdir -p /backup/restore-data

# Убедитесь, что нет файла с тем же именем
if [ -f "$LOCAL_BACKUP_FILE" ]; then
  echo "Warning: A file already exists at $LOCAL_BACKUP_FILE. It will be overwritten."
fi

# Скачивание файла из хранилища
echo "Downloading backup file from $REMOTE_BACKUP_FILE to $LOCAL_BACKUP_FILE..."
rclone copy selectel:$REMOTE_BACKUP_FILE /backup/restore-data -v --log-file=/backup/rclone.log

# Дополнительная проверка на существование файла
if [ ! -f "$LOCAL_BACKUP_FILE" ]; then
  echo "Error: The backup file was not found after the download."
  exit 1
fi

# Восстановление базы данных из файла .backup
echo "Restoring the database from $LOCAL_BACKUP_FILE..."
PGPASSWORD=$DB_PASSWORD pg_restore -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -v $LOCAL_BACKUP_FILE > restore_log.txt 2>&1

echo "Database restoration completed successfully."