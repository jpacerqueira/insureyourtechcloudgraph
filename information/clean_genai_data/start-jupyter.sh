#!/bin/bash 
#
echo "Move latest Outages abd Service Ratings to folder of : data/"
cp -rf ../../cloud-services-risk-ratings-api/data/*.csv data/
#
echo "start Container Jypter"
docker container run -it  --mount type=bind,src=$(pwd),dst=/home/jovyan/work --rm -p 8888:8888   jupyter/base-notebook
#