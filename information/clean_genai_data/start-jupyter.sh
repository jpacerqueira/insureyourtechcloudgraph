	
docker container run -it  --mount type=bind,src=$(pwd)/data,dst=/home/jovyan/work/data --rm -p 8888:8888   jupyter/base-notebook
