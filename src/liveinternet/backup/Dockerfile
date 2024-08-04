FROM alpine:latest

# Установите необходимые утилиты
RUN apk update && apk add postgresql-client rclone bash curl

# Скопируйте скрипты в контейнер
COPY backup.sh /usr/local/bin/backup.sh
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Сделайте скрипты исполняемыми
RUN chmod +x /usr/local/bin/backup.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Настройка точки входа
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]