## Inspect each layer of a docker image

```
brew install dive
dive nginx:latest
```

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

## Clean docker builder cache to release storage

```
docker builder prune
```


## Check docker container info by a host process (which consumes nvidia vram), 

Check the container info of cgroup on Linux:
cat /proc/460246/cgroup

By one liner command:
``` bash
docker ps --filter id=$(cat /proc/460246/cgroup | grep docker | head -1 | sed 's/.*docker[/-]\([a-f0-9]\{64\}\).*/\1/' | cut -c1-12) --format "table {{.Names}}\t{{.ID}}\t{{.Image}}\t{{.Status}}"
```

 docker_ps.sh
``` bash
#!/bin/bash

# docker_ps.sh - Get Docker container info by host process ID
# Usage: docker_ps.sh <process_id>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <process_id>"
    echo "Example: $0 460246"
    exit 1
fi

PROCESS_ID=$1

# Check if process exists
if [ ! -d "/proc/$PROCESS_ID" ]; then
    echo "Error: Process ID $PROCESS_ID not found"
    exit 1
fi

# Extract container ID from cgroup
CONTAINER_ID=$(cat /proc/$PROCESS_ID/cgroup 2>/dev/null | grep -o 'docker[/-][a-f0-9]\{64\}' | head -1 | sed 's/docker[/-]//')

if [ -z "$CONTAINER_ID" ]; then
    echo "Process ID $PROCESS_ID is not running in a Docker container"
    exit 1
fi

# Get short container ID (first 12 characters)
SHORT_ID=${CONTAINER_ID:0:12}

# Get container information
CONTAINER_INFO=$(docker ps --filter id=$SHORT_ID --format "table {{.Names}}\t{{.ID}}\t{{.Image}}\t{{.Status}}" --no-trunc)

if [ -z "$CONTAINER_INFO" ] || [ "$CONTAINER_INFO" = "NAMES	CONTAINER ID	IMAGE	STATUS" ]; then
    echo "Container with ID $SHORT_ID not found in running containers"
    echo "Container might be stopped. Checking all containers..."
    docker ps -a --filter id=$SHORT_ID --format "table {{.Names}}\t{{.ID}}\t{{.Image}}\t{{.Status}}"
else
    echo "$CONTAINER_INFO"
fi
```
