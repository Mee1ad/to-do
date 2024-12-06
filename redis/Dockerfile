FROM redis:alpine

COPY sysctl.conf /etc/sysctl.conf

RUN sysctl -p /etc/sysctl.conf

EXPOSE 6379

CMD ["redis-server", "--requirepass", "${REDIS_PASSWORD}", "--save", "60", "1", "--loglevel", "warning"]
