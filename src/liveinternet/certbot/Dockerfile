FROM certbot/certbot:v2.6.0

RUN mkdir "/var/www/certbot/www/.well-known"
RUN mkdir "/var/www/certbot/www/.well-known/acme-challenge"

RUN mkdir "scripts"

COPY get_cert_and_update_nginx.sh /scripts

RUN chmod +x get_cert_and_update_nginx.sh
