FROM mysql:8

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=xss
ENV MYSQL_USER=webmaster
ENV MYSQL_PASSWORD=securep

COPY ./database.sql /docker-entrypoint-initdb.d/database.sql

EXPOSE 3306
