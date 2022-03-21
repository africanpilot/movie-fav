
FROM node:buster

# Default environment
ARG APP_MOUNT_URI='http://localhost:3000'
ENV PATH "$PATH:/home/moviefav/.local/bin"
ENV NODE_ENV='production'

RUN groupmod -g 1000 node && usermod -u 1000 -g 1000 node
RUN usermod -d /home/moviefav -m -l moviefav node
ENV HOME /home/moviefav

ENV NPM_CONFIG_PREFIX=/home/moviefav/.npm-global
ENV PATH=$PATH:/home/moviefav/.npm-global/bin

RUN mkdir -p /home/moviefav/client
RUN touch /home/moviefav/is_client

COPY . /home/moviefav/client/
RUN chown -R moviefav /home/moviefav/client
USER moviefav
WORKDIR /home/moviefav/client

RUN npm install npm@latest && \
    npm run build