FROM certbot/certbot

RUN apk add --no-cache nginx certbot-nginx

COPY get_or_renew_certs.sh /get_or_renew_certs.sh

ENTRYPOINT ["/entrypoint.sh"]
