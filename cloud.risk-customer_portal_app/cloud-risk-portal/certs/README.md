
 Insert instructions here

    - generate key and cert
    - copy to certs folder
    - update server.js to use certs
    - update Dockerfile to expose ports 8184 and 443
    - update docker-compose file to use certs

 Run the following to generate key and cert , with a 10 year expiration

cat >> openssl.cnf <<EOF
[ req ]
prompt = no
distinguished_name = simulation_insureyourtech_dotcloud 

[ simulation_insureyourtech_dotcloud ]
C = GB
ST = London
L = London
O = InsureYourTech
OU = Cloud Services
CN = simulation.cloud.risk.insureyourtech.cloud
emailAddress = business@insureyourtech.com
EOF

 # openssl req  -config openssl.cnf   -days 3650 -nodes -new -x509 -keyout server8184.key -out server8184.cert