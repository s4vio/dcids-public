#https://hub.docker.com/_/redis?tab=description&page=1&ordering=last_updated

FROM redis:6.2.4-alpine

COPY redis.conf /usr/local/etc/redis/redis.conf

RUN mkdir /var/log/redis && chmod 777 /var/log/redis

CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
