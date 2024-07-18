FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

# Устанавливаем certbot для управления сертификатами
# Устанавливаем snapd и certbot
RUN apt-get update && \
    apt-get remove certbot && \
    apt-get install -y certbot python3-certbot-nginx

# Добавляем символьную ссылку и запускаем настройку нгинкса
RUN ln -s /snap/bin/certbot /usr/bin/certbot && sudo certbot --nginx
