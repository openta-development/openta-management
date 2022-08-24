FROM python:3.9

RUN apt-get update \
    && apt-get install -y \
    graphviz \
    libcairo2 \
    libcairo2-dev \
    libgraphviz-dev \
    libjpeg-dev \
    libxml2-dev \
    libxslt1-dev \
    libzmq3-dev \
    memcached  \
    libmemcached-dev  \
    vim \
    postgresql-13 \
    postgresql-client-13 \
    rsync \
    apt-utils \
    redis \
    libnss3 \
    poppler-utils

COPY requirements-openta-management.txt /srv/servermanager/requirements.txt
WORKDIR /srv/servermanager
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install --yes --no-install-recommends ca-certificates curl gpg 
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - 
RUN apt-get update 
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" | tee   /etc/apt/sources.list.d/pgdg.list
