FROM redis:alpine

COPY sysctl.conf /etc/sysctl.conf

RUN sysctl -p /etc/sysctl.conf

EXPOSE 6379

CMD ["redis-server"]
