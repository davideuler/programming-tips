
## Remove dangling docker images with a none tag

```
docker images -a | grep none | awk '{ print $3; }' | xargs docker rmi

# or run by root:
sudo docker images -a | grep none | awk '{ print $3; }' | xargs sudo docker rmi
```

## Debug a Dockerfile from current directory:

Mount the current directory to container of base image, then run command in dockerfile one by one.

```
docker run --rm -it --mount type=bind,source="$(pwd)"/,target=/src ubuntu:22.04 /bin/bash
```

## Check files, and files size in a volume

```
docker volume create --name postgres-data
docker volume ls
docker volume inspect postgres-data
docker run --rm -i -v=postgres-data:/tmp/myvolume busybox find /tmp/myvolume
docker run --rm -i -v=postgres-data:/tmp/myvolume busybox du -sh /tmp/myvolume
docker run -it --name admin -v postgres-data:/var/lib/postgresql/data ubuntu

```

## Get command used to start a Docker container

https://stackoverflow.com/questions/32758793/how-to-show-the-run-command-of-a-docker-container

docker inspect facechain |  jq -r '.[0]["Config"]["Cmd"][0]'

## How to start a stopped Docker container

docker start facechain

## How to start a stopped Docker container with a different command?

Find the stopped container, commit the stopped container to a new image. 
And start a new container of the image.

```
docker ps -a
docker commit $CONTAINER_ID user/test_image
docker run -ti --entrypoint=/bin/bash user/test_image

```