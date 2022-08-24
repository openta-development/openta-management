FROM opentaproject/openta-base:v980
WORKDIR /srv/openta/servermanager
COPY . /srv/openta
EXPOSE 8000
