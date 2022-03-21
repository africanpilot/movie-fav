FROM python:3.10-slim-buster

# Default environment
# ARG MOVIE_FAV_ENV='dev'
# ENV MOVIE_FAV_ENV=$MOVIE_FAV_ENV

ENV PATH "$PATH:/home/moviefav/.local/bin"
USER root

#
# This section is just here to make testing network stuff inside the container easier.
# We can drop it later.
#
RUN \
 apt update && \
 apt install -y librdkafka-dev && \
\
 apt install -y net-tools && \
 apt install -y iputils-ping && \
 apt install -y telnet && \
 apt install -y procps && \
 apt install -y nano && \
\
 apt-get autoremove && \
 apt-get clean && \
 apt-get install -y libmagickwand-dev --no-install-recommends && \
 rm -rf /var/lib/apt/lists/* && \
\
 groupadd -g 1000 moviefav && \
 useradd -u 1000 -g 1000 -ms /bin/bash moviefav

USER moviefav
WORKDIR   /home/moviefav
ENV HOME  /home/moviefav
RUN mkdir /home/moviefav/server
COPY requirements.txt /home/moviefav/server
RUN \
  touch /home/moviefav/is_apps && \
  pip install --upgrade pip && \
  pip install --user --requirement /home/moviefav/server/requirements.txt

USER root
ARG CACHEBUST=1
COPY . /home/moviefav/server
RUN \
  /home/moviefav/server/tools/build_root.sh
USER moviefav
ENV /home/moviefav/.profile /bin/sh