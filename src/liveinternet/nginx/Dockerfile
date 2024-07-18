FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

# Устанавливаем certbot для управления сертификатами
# Устанавливаем snapd и certbot
RUN apt-get update && \
    apt-get install -y snapd && \
    snap install core && \
    snap install --classic certbot && \
    ln -s /snap/bin/certbot /usr/bin/certbot

# Добавляем символьную ссылку и запускаем настройку нгинкса
RUN ln -s /snap/bin/certbot /usr/bin/certbot && sudo certbot --nginx
