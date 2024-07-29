# Используем образ certbot на основе Alpine Linux
FROM certbot/certbot:v2.6.0

RUN mkdir "scripts"

COPY renew_certificates.sh /scripts

RUN chmod chmod +x scripts/renew_certificates.sh
