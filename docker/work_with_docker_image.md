
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
