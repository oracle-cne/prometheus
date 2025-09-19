#!/usr/bin/env bash

name="prometheus"
version="3.5.0"
registry="container-registry.oracle.com/olcne"
docker_tag=${registry}/${name}:v${version}

# Copy the promu tool from the container image
mkdir -p bin
podman create --pull always --name tmpcopy container-registry.oracle.com/olcne/promu:v0.17.0
podman cp tmpcopy:/bin/promu bin/promu
podman rm tmpcopy

patch < olm/package.json.patch

docker build --pull \
    --build-arg https_proxy=${https_proxy} \
    -t ${docker_tag} -f ./olm/builds/Dockerfile .
docker save -o ${name}.tar ${docker_tag}
