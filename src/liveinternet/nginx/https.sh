#!/bin/bash

# Путь к файлу, который нужно обработать
FILE="/home/stat_mil_ru/project/src/liveinternet/nginx/nginx.conf"

# Проверяем, существует ли файл
if [ -f "$FILE" ]; then
  # Удаляем все символы # и сохраняем изменения в файле
  sed -i 's/#//g' "$FILE"
  echo "Все символы # удалены из файла $FILE."
else
  echo "Файл $FILE не найден."
fi
