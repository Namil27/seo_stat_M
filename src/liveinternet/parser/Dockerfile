FROM python:3.9-slim

WORKDIR /app

# Установка cron и других необходимых пакетов
RUN apt-get update && apt-get install -y cron

# Копирование файла зависимостей и установка зависимостей
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего приложения в контейнер
COPY . .

# Запуск cron
CMD ["/app/start.sh"]