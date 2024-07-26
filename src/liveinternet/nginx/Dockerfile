FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir /var/www/certbot/.well-known
RUN mkdir /var/www/certbot/.well-known/acme-challenge