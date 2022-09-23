FROM opentaproject/openta-management-base:v990
WORKDIR /srv/openta/servermanager
COPY . /srv/openta
EXPOSE 8000
