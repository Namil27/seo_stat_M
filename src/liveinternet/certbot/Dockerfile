FROM certbot/certbot

RUN apk add --no-cache nginx certbot-nginx

COPY get_or_renew_certs.sh /get_or_renew_certs.sh

RUN chmod ugo+x get_ot_renew_certs.sh

ENTRYPOINT ["/get_or_renew_certs.sh"]
