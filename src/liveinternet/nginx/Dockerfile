FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

# Устанавливаем certbot для управления сертификатами
# Устанавливаем snapd и certbot
RUN apt-get update && \
    apt-get remove certbot && \
    apt-get install -y certbot python3-certbot-nginx

RUN mkdir -p /etc/letsencrypt && \
    wget -O /etc/letsencrypt/options-ssl-nginx.conf https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf

# Добавляем символьную ссылку и запускаем настройку нгинкса
RUN certbot --nginx
