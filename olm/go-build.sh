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

patch  --no-backup-if-mismatch -p0 --fuzz=0 < olm/package.json.patch
yq -i '.build.flags = "-trimpath=false"' .promu.yml
yq -i '.build.ldflags += "-X main.version=v${version}"' .promu.yml

echo "npm version"
npm version
echo "node --version"
node --version
echo "yarn --version"
yarn --version
go version


make assets npm_licenses assets-compress plugins
promu build
