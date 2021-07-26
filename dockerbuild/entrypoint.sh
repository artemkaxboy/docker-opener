#!/bin/sh

##################### FUNCTIONS

die() {
    echo >&2 "$@"
    exit 1
}

find_container() {
    ###### find by exact name
    target_id=$(docker ps --filter name=^"$1"$ -q)
    [ -n "$target_id" ] && echo "Found container with name: $1"

    ###### find by name
    if [ -z "$target_id" ]; then
        target_id=$(docker ps --no-trunc --format "{{.ID}} {{.Names}}" | grep "\\s.*$1" -m1 | awk '{print $1}')
        [ -n "$target_id" ] && echo "Found container with name containing: $1"
    fi

    ###### find by image
    if [ -z "$target_id" ]; then
        target_id=$(docker ps --no-trunc --format "{{.ID}} {{.Image}}" | grep "\\s.*$1" -m1 | awk '{print $1}')
        [ -n "$target_id" ] && echo "Found container with image containing: $1"
    fi

    ###### find by id
    if [ -z "$target_id" ]; then
        target_id=$(docker ps --no-trunc --format "{{.ID}} {{.ID}}" | grep "\\s.*$1" -m1 | awk '{print $1}')
        [ -n "$target_id" ] && echo "Found container with ID containing: $1"
    fi

    ###### find by port
    if [ -z "$target_id" ]; then
        target_id=$(docker ps --no-trunc --format "{{.ID}} {{.Ports}}" | grep "\\s.*$1" -m1 | awk '{print $1}')
        [ -n "$target_id" ] && echo "Found container with port containing: $1"
    fi

    if [ -z "$target_id" ]; then
        die "Container not found: $1"
    fi

    docker ps --filter id="$target_id"
}

connect() {
    [ "$#" -eq 0 ] && die "Target required"
    [ "$#" -gt 1 ] && die "Only one target expected"
    find_container "$1"

    docker exec --user 0 "$target_id" bash > /dev/null && interpreter="bash"
    [ -z "$interpreter" ] && docker exec --user 0 "$target_id" sh > /dev/null && interpreter="sh"

    case $interpreter in
        bash|sh)
            connect_only $interpreter ;;
        *) install_busybox_and_connect ;;
    esac
}

connect_only() {
    echo "Native shell found: $1"
    echo "Connecting..."
    docker exec --user 0 -it "$target_id" "$1"
}

install_busybox_and_connect() {
    install_busybox

    # runs if any interrupt, terminate, exit signal come. Doesn't work with docker kill
    trap remove_busybox INT TERM EXIT

    echo "Connecting..."
    docker exec --user 0 -it "$target_id" /busybox sh -c '
        export PATH="/busybin:$PATH"
        /busybox mkdir /busybin -p
        /busybox --install /busybin
        sh'
}

install_busybox() {
    echo "Installing busybox..."
    docker cp /busybox "$target_id":/busybox
}

remove_busybox() {
    echo "Removing busybox..."
    docker exec --user 0 -it "$target_id" /busybin/rm -rf /busybox /busybin
}

fetch_logs() {
    [ "$#" -eq 0 ] && die "Target required"

    find_container "$1"
    echo "Fetching logs for $target_id"
    shift

    docker logs "$target_id" "$@"
}

##################### START
# stop on any error
# set -e

case $1 in
    logs)
        shift
        fetch_logs "$@" ;;
    --)
        shift
        connect "$@" ;;
    *) connect "$@" ;;
esac
