	
docker container run -it  --mount type=bind,src=$(pwd),dst=/home/jovyan/work --rm -p 8888:8888   jupyter/base-notebook
