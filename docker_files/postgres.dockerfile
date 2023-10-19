FROM postgres:15.3-alpine3.18

COPY database/*.sql /docker-entrypoint-initdb.d/