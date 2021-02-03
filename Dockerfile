FROM python:3.7-alpine

ADD . /push/

WORKDIR /push/api

RUN apk update \
  && apk add tzdata wget redis tar gcc make g++ libffi-dev openssl-dev --no-cache \
  && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
  && echo "Asia/Shanghai" > /etc/timezone \
  && pip install -r requirements.txt \
  && caddy_tag=2.2.1 \
  && wget -N https://github.com/caddyserver/caddy/releases/download/v${caddy_tag}/caddy_${caddy_tag}_linux_amd64.tar.gz \
  && tar -zxvf caddy_${caddy_tag}_linux_amd64.tar.gz \
  && mv caddy /usr/local/bin/ \
  && rm -rf caddy_${caddy_tag}_linux_amd64.tar.gz \
  && echo -e ":80 \n\
root * /push/dist \n\
encode gzip zstd \n\
file_server \n\
route /push/* { \n\
    uri strip_prefix /push \n\
    reverse_proxy 127.0.0.1:5000 \n\
} \n\
log { \n\
    output file /push/logs/access.log \n\
    format single_field common_log \n\
} \n\
@notAPI { \n\
    not { \n\
        path /push/* \n\
    } \n\
    file { \n\
        try_files {path} /index.html \n\
    } \n\
} \n\
rewrite @notAPI {http.matchers.file.relative} \n" > /push/Caddyfile \
  && echo  -e "redis-server & \n\
/usr/local/bin/caddy run --config /push/Caddyfile & \n\
python -u app.py > /push/logs/log.out 2>&1 & \n\
tail -f /push/logs/log.out \n" > /push/start.sh \
  && chmod +x /push/start.sh \
  && apk del tzdata wget tar gcc make g++ libffi-dev openssl-dev \
  && rm -rf /var/cache/apk/* \
  && rm -rf /root/.cache/*

CMD ["sh","/push/start.sh"]

EXPOSE 80
