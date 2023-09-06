FROM debian:bullseye

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get -y install build-essential \
        zlib1g-dev \
        libncurses5-dev \
        libgdbm-dev \ 
        libnss3-dev \
        libssl-dev \
        libreadline-dev \
        libffi-dev \
        libsqlite3-dev \
        libbz2-dev \
        wget \
        sqlite3 \
        ffmpeg \ 
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get purge -y imagemagick imagemagick-6-common 

RUN cd /usr/src \
    && wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz \
    && tar -xzf Python-3.11.0.tgz \
    && cd Python-3.11.0 \
    && ./configure --enable-optimizations \
    && make altinstall

RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 1

RUN curl -sS -O https://bootstrap.pypa.io/get-pip.py | python3.11

RUN mkdir /app

COPY requirements.txt /app
COPY reddit-bot/ /app

RUN python3.11 -m pip install -r /app/requirements.txt --no-cache-dir
WORKDIR /app
RUN sqlite3 db.sqlite3 < db.sql
CMD python3.11 main.py
