#!/bin/sh

# Получаем сертификат
certbot certonly --webroot -w /var/www/certbot -d stat.miliutin.ru --non-interactive --agree-tos --email namil05@yandex.ru

# Проверяем успешность выполнения команды certbot
if [ $? -eq 0 ]; then
    # Путь к конфигурационному файлу Nginx
    CONFIG_FILE="/etc/nginx/nginx.conf"

    # Создаем временный файл для хранения результатов
    TEMP_FILE=$(mktemp)

    # Удаляем все символы # из файла
    sed 's/#//g' "$CONFIG_FILE" > "$TEMP_FILE"

    # Заменяем оригинальный файл временным файлом
    mv "$TEMP_FILE" "$CONFIG_FILE"

    echo "Все символы # удалены из файла $CONFIG_FILE"
else
    echo "Ошибка: Не удалось получить сертификат."
fi
