
 Insert instructions here

    - generate key and cert
    - copy to certs folder
    - update server.js to use certs
    - update Dockerfile to expose ports 8184 and 443
    - update docker-compose file to use certs

 Run the following to generate key and cert , with a 10 year expiration
 
  openssl req  -days 3650 -nodes -new -x509 -keyout server.key -out server.cert