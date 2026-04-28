#!/usr/bin/env bash

name="prometheus"
version="3.11.3"
registry="container-registry.oracle.com/olcne"
docker_tag=${registry}/${name}:v${version}

# Copy the promu tool from the container image
mkdir -p bin
podman create --pull always --name tmpcopy container-registry.oracle.com/olcne/promu:v0.17.0
podman cp tmpcopy:/bin/promu bin/promtool
podman rm tmpcopy

podman build --pull \
    --build-arg https_proxy=${https_proxy} \
    --volume /etc/yum.repos.d:/etc/yum.repos.d \
    --volume ~/.npmrc:/.npmrc \
    -t ${docker_tag} -f ./olm/builds/Dockerfile .
podman save -o ${name}.tar ${docker_tag}
