#!/usr/bin/env bash

mkdir -p bin
version="3.5.0"

GIT_REVISION=$(git rev-parse HEAD)
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
ldflags="
        -X main.version=v${version}
        -X github.com/prometheus/common/version.Version=${version}
        -X github.com/prometheus/common/version.Revision=${GIT_REVISION}
        -X github.com/prometheus/common/version.Branch=HEAD
        -X github.com/prometheus/common/version.BuildUser=${USER}@${HOST}
        -X github.com/prometheus/common/version.BuildDate=${BUILD_DATE}"

patch < olm/package.json.patch
node --version
npm --version
yarn --version
go --version

make build

#go build -trimpath=false -v -o bin/ \
#    -ldflags "${ldflags}" \
#    "${GOPATH_SRC}"/cmd/alertmanager \
#    "${GOPATH_SRC}"/cmd/amtool
