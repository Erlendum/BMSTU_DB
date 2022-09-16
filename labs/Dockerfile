FROM postgres:alpine
ADD lab_01/01_create.sql /docker-entrypoint-initdb.d
ADD lab_01/02_constraints.sql /docker-entrypoint-initdb.d
ADD lab_01/03_copy.sql /docker-entrypoint-initdb.d
ADD data /docker-entrypoint-initdb.d
RUN ls /docker-entrypoint-initdb.d
RUN chmod a+r /docker-entrypoint-initdb.d/*
EXPOSE 6666
