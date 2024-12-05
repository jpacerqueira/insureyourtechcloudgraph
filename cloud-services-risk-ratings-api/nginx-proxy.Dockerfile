FROM nginx:1.27-perl

COPY certs /etc/nginx/certs/
RUN chmod 600 /etc/nginx/certs/server8183.key /etc/nginx/certs/server8183.cert
RUN chmod 600 /etc/nginx/certs/server8183.key /etc/nginx/certs/server8183.cert
