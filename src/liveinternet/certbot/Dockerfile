FROM certbot/certbot

RUN apk add --no-cache nginx certbot-nginx

RUN mkdir scripts

COPY get_or_renew_certs.sh /scripts/get_or_renew_certs.sh

RUN chmod ugo+x get_or_renew_certs.sh

ENTRYPOINT ["/get_or_renew_certs.sh"]
