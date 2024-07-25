FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

# Устанавливаем certbot для управления сертификатами
# Устанавливаем snapd и certbot
RUN rm /etc/apt/preferences.d/nosnap.pref && \
    apt-get remove certbot && \
    apt-get update && \
    apt install snapd && \
    snap install --classic certbot && \
    certbot --nginx

# RUN mkdir -p /etc/letsencrypt && \
#    wget -O /etc/letsencrypt/options-ssl-nginx.conf https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf
