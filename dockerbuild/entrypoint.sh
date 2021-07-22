#!/bin/sh

die () {
    echo >&2 "$@"
    exit 1
}

# stop on any error
set -e

[ "$#" -eq 1 ] || die "One argument required"

###### find by exact name
target_id=$(docker ps --filter name=^"$1"$ -q)
[ -n "$target_id" ] && echo "Found container with name: $1"

###### find by name
if [ -z "$target_id" ]; then
    target_id=$(docker ps --no-trunc --format "{{.ID}} {{.Names}}" | grep "\\s.*$1" | head -n1 | awk '{print $1}')
    [ -n "$target_id" ] && echo "Found container with name containing: $1"
fi

###### find by image
if [ -z "$target_id" ]; then
    target_id=$(docker ps --no-trunc --format "{{.ID}} {{.Image}}" | grep "\\s.*$1" | head -n1 | awk '{print $1}')
    [ -n "$target_id" ] && echo "Found container with image containing: $1"
fi

###### find by id
if [ -z "$target_id" ]; then
    target_id=$(docker ps --no-trunc --format "{{.ID}} {{.ID}}" | grep "\\s.*$1" | head -n1 | awk '{print $1}')
    [ -n "$target_id" ] && echo "Found container with ID containing: $1"
fi

###### find by port
if [ -z "$target_id" ]; then
    target_id=$(docker ps --no-trunc --format "{{.ID}} {{.Ports}}" | grep "\\s.*$1" | head -n1 | awk '{print $1}')
    [ -n "$target_id" ] && echo "Found container with port containing: $1"
fi

if [ -z "$target_id" ]; then
    die "Container not found: $1"
fi

docker ps --filter id="$target_id"

docker cp /busybox "$target_id":/busybox

# runs if any interrupt, terminate, exit signal come. Doesn't work with docker kill
trap 'docker exec --user root -it "$target_id" /busybin/rm -rf /busybox /busybin' INT TERM EXIT

docker exec --user root -it "$target_id" /busybox sh -c '
export PATH="/busybin:$PATH"
/busybox mkdir /busybin -p
/busybox --install /busybin
sh'
