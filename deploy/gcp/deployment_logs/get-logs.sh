#/bin/bash env
#
echo "Get Logs - API Databases & Customer-Portal "
#
cd cloud-services-risk-ratings-api
docker-compose logs > build-api-cluster.log
cp -rf build-api-cluster.log ~  
cd ..
#
cd cloud.risk-customer_portal_app 
docker-compose logs > customer-app-start.log 
cp -rf customer-app-start.log ~
cd ..
#
ls -listarh *.log 
