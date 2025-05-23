

## 1.How to install buildx plugin

It works for docker, and also for colima.

TLDR:
Just download it from https://github.com/docker/buildx/releases/, uncompress the executable, and put it to ~/.docker/cli-plugins.

Installation script: install_buildx.sh

```bash
#!/bin/bash

# Docker Buildx Installation Script for Linux and macOS
# Supports both x86_64/amd64 and ARM64 architectures

VERSION=v0.24.0

#ARCH=arm64 # change to 'arm64' for m1, amd64 on amd64
#VERSION=v0.24.0
#curl -LO https://github.com/docker/buildx/releases/download/${VERSION}/buildx-${VERSION}.darwin-${ARCH}
#mkdir -p ~/.docker/cli-plugins
#mv buildx-${VERSION}.darwin-${ARCH} ~/.docker/cli-plugins/docker-buildx
#chmod +x ~/.docker/cli-plugins/docker-buildx
#docker buildx version # verify installation


# Detect operating system
OS=""
case "$(uname -s)" in
    Darwin*)
        OS="darwin"
        ;;
    Linux*)
        OS="linux"
        ;;
    *)
        echo "Unsupported operating system: $(uname -s)"
        exit 1
        ;;
esac

# Detect architecture
ARCH=""
case "$(uname -m)" in
    x86_64|amd64)
        ARCH="amd64"
        ;;
    arm64|aarch64)
        ARCH="arm64"
        ;;
    *)
        echo "Unsupported architecture: $(uname -m)"
        exit 1
        ;;
esac

echo "Detected OS: $OS  Detected Architecture: $ARCH"
echo "Installing Docker Buildx version: $VERSION"

BUILDX_FILE="buildx-${VERSION}.${OS}-${ARCH}"
DOWNLOAD_URL="https://github.com/docker/buildx/releases/download/${VERSION}/${BUILDX_FILE}"

echo "Downloading from: $DOWNLOAD_URL"
curl -LO "$DOWNLOAD_URL"

if [ $? -ne 0 ]; then
    echo "Failed to download buildx"
    exit 1
fi

mkdir -p ~/.docker/cli-plugins
mv "$BUILDX_FILE" ~/.docker/cli-plugins/docker-buildx
chmod +x ~/.docker/cli-plugins/docker-buildx

# Verify installation
echo "Verifying installation..."
docker buildx version

```

## 2.How to run buildx in docker compose:
COMPOSE_DOCKER_CLI_BUILD=1 \
DOCKER_BUILDKIT=1 \
DOCKER_DEFAULT_PLATFORM=linux/amd64 \
docker-compose build

example
COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 DOCKER_DEFAULT_PLATFORM=linux/amd64 docker compose --env-file .env -f docker-compose-full-exp.yml build

## 3.Reference

https://aosolorzano.medium.com/installing-colima-as-a-docker-engine-provider-with-buildx-and-compose-plugins-installed-1ce8b3bae158
https://stackoverflow.com/questions/59756123/use-buildx-build-linux-arm64-in-docker-compose-file
https://github.com/docker/buildx/releases/
