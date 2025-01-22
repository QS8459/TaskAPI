FROM alpine:latest

RUN apk --no-cache update sudo bash && \
    apk add nano \
    postgresql15 postgresql15-contrib postgresql15-openrc postgresql15-client libpq su-exec tzdata\
    postgresql-url_encode && \
    rm -rf /var/cache/apk/* && \
    mkdir /docker-entrypoint-initdb.d

RUN addgroup -S taskapi && adduser taskapi -S -G taskapi taskapi

RUN echo "taskapi:admin" |chpasswd

RUN echo "taskapi ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

ENV LANG en_GB.utf8
ENV PGDATA /var/lib/postgresql/data

VOLUME /var/lib/postgresql/data

COPY docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 5432

RUN chmod -R 755 /docker-entrypoint.sh && \
    mkdir -p /run/postgresql && \
    chown postgres: /run/postgresql


# USER postgres

WORKDIR /home/taskapi

CMD ["postgres"]