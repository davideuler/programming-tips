
You can use docker buildx to cross build images for various architecture. e.g.

```
# first create a builder, and use the new one, then build image for specific platform
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t myreg/fancyimage:latest --output=type=registry,registry.insecure=true Dockerfile
```

https://docs.docker.com/build/building/drivers/

https://github.com/docker/buildx/blob/master/docs/reference/buildx_create.md
