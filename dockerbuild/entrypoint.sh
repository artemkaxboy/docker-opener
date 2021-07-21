#!/bin/sh

# stop on any error
set -e

docker ps --filter name=$1
target_id=$(docker ps --filter name=$1 -ql)
echo Target container id: $target_id

docker cp /busybox $target_id:/busybox

# runs if any interrupt, terminate, exit signal come. Doesn't work with docker kill
trap "docker exec -it $target_id /busybin/rm -rf /busybox /busybin" INT TERM EXIT

docker exec -it $target_id /busybox sh -c '
export PATH="/busybin:$PATH"
/busybox mkdir /busybin -p
/busybox --install /busybin
sh'
