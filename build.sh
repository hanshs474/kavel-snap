#!/bin/sh
# Cross-compile the kavel-go CLI and pack one snap per architecture.
set -e
for a in amd64 arm64; do
  mkdir -p build/$a/meta && sed "s/ARCH/$a/" snap.yaml > build/$a/meta/snap.yaml
  CGO_ENABLED=0 GOOS=linux GOARCH=$a go -C ../kavel-go build -trimpath -ldflags="-s -w" -o "$PWD/build/$a/bin/kavel" ./example
done
docker run --rm -v "$PWD/build:/b" ubuntu:22.04 sh -c 'apt-get update -qq && apt-get install -y -qq squashfs-tools >/dev/null &&
  for a in amd64 arm64; do mksquashfs /b/$a /b/kavel_0.1.0_$a.snap -noappend -comp xz -all-root -no-xattrs -no-fragments -quiet; done'
