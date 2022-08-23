FROM opentaproject/openta-base:v950
WORKDIR /srv/openta/servermanager
COPY . /srv/openta
EXPOSE 8000
