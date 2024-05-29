# Используйте официальный образ Python как базовый
FROM python:3.9-slim

# Установите рабочую директорию в контейнере
WORKDIR /app

# Установите системные зависимости
RUN apt-get update \
    && apt-get -y install gcc libpq-dev \
    && apt-get clean

# Копируйте файл зависимостей первым, чтобы кешировать установку зависимостей
COPY requirements.txt .

# Установите зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте остальные файлы проекта в рабочую директорию
COPY . .