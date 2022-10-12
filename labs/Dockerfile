FROM postgres:latest
RUN apt-get update
RUN apt-get -y install python3 postgresql-contrib postgresql-plpython3-14
ADD lab_01/01_create.sql /docker-entrypoint-initdb.d
ADD lab_01/02_constraints.sql /docker-entrypoint-initdb.d
ADD lab_01/03_copy.sql /docker-entrypoint-initdb.d
ADD data /docker-entrypoint-initdb.d
RUN chmod a+r /docker-entrypoint-initdb.d/*
EXPOSE 6666
