# Dockerfile for Certbot
FROM certbot/certbot

# Копируем скрипт получения и обновления сертификатов
COPY get_or_renew_certs.sh /usr/bin/get_or_renew_certs.sh

# Делаем скрипт исполняемым
RUN chmod +x /usr/bin/get_or_renew_certs.sh

# Настраиваем точку входа для автоматического обновления сертификатов
ENTRYPOINT ["/usr/bin/get_or_renew_certs.sh"]
