FROM nginx:stable-alpine

        COPY conf/nginx-certbot-init.conf /etc/nginx/nginx-certbot-init.conf
        COPY conf/default.conf /etc/nginx/conf.d/

        ENTRYPOINT ["nginx", "-g", "daemon off;"]
        
