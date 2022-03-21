FROM node:buster

# Default environment
ENV PATH "$PATH:/home/moviefav/.local/bin"
ENV NODE_ENV='production'

RUN apt update && \
apt install -y net-tools && \
apt install -y iputils-ping && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

#
# Node image has a node user that must be changed for our purposes...
#

RUN groupmod -g 1000 node && usermod -u 1000 -g 1000 node
RUN usermod -d /home/moviefav -m -l moviefav node
ENV HOME /home/moviefav
USER moviefav

ENV NPM_CONFIG_PREFIX=/home/moviefav/.npm-global
ENV PATH=$PATH:/home/moviefav/.npm-global/bin

RUN mkdir -p /home/moviefav/apollo
RUN touch /home/moviefav/is_apollo

WORKDIR /home/moviefav/apollo

#COPY package*.json ./ nodemon@2.0.2
RUN npm install npm@latest --production
RUN npm install @apollo/gateway apollo-server graphql dotenv
# RUN npm install @apollo/gateway@0.47.0 apollo-server@3.6.2 graphql@16.3.2 apollo-server-core@3.3.0

ARG CACHEBUST=1
COPY . /home/moviefav/apollo

EXPOSE 4000

# CMD ["npm", "run", "start-gateway"]
CMD ["npm", "run", "start-gateway-production"]
