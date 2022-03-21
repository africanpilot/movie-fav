FROM nginx

RUN apt update && \
apt install -y jq && \
rm -rf /var/lib/apt/lists/* && \
mkdir -p /etc/nginx/moviefav/locations

COPY conf/nginx.conf /etc/nginx/nginx.conf
COPY conf/default.conf /etc/nginx/conf.d/
COPY spin.sh /tmp

COPY tools/nginx_start.sh /docker-entrypoint.d/02-nginx_start.sh
RUN chmod 775 /docker-entrypoint.d/02-nginx_start.sh