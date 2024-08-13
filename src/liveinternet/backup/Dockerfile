FROM ubuntu:latest

# Установите необходимые утилиты
RUN apt update && apt install -y postgresql-client rclone bash curl cron

# Создайте необходимые директории
RUN mkdir -p /backup
RUN mkdir -p /root/.config/rclone

# Скопируйте скрипты и конфигурационные файлы в контейнер
COPY backup.sh /backup/backup.sh
COPY entrypoint.sh /backup/entrypoint.sh
COPY restore.sh /backup/restore.sh
COPY rclone.conf /root/.config/rclone/rclone.conf

# Сделайте скрипты исполняемыми
RUN chmod +x /backup/backup.sh
RUN chmod +x /backup/entrypoint.sh
RUN chmod +x /backup/restore.sh

# Настройка точки входа
ENTRYPOINT ["/backup/entrypoint.sh"]