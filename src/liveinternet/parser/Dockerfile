FROM python:3.9-slim

WORKDIR /app

# Установка cron и других необходимых пакетов
RUN apt-get update && apt-get install -y cron

# Копирование файла зависимостей и установка зависимостей
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего приложения в контейнер
COPY . .

# Добавление cron задачи
COPY crontab /etc/cron.d/parser-cron
RUN chmod 0644 /etc/cron.d/parser-cron
RUN crontab /etc/cron.d/parser-cron

# Установка прав на выполнение для wrapper.sh
RUN chmod +x /app/wrapper.sh

# Запуск cron
CMD ["cron", "-f"]
