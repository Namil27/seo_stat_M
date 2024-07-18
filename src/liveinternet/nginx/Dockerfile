FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

# Устанавливаем certbot для управления сертификатами
RUN apt-get update && apt-get install snapd && apt-get remove certbot && snap install --classic certbot

# Добавляем символьную ссылку и запускаем настройку нгинкса
RUN ln -s /snap/bin/certbot /usr/bin/certbot && sudo certbot --nginx
