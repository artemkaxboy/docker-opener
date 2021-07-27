#!/bin/sh

# shebang
# /bin/bash breaks container starting, because container does not have /bin/bash
# /bin/sh breaks running script on host, because some bashism is not supported by /bin/sh

# bashism
# https://tldp.org/LDP/abs/html/parameter-substitution.html

##################### FUNCTIONS

die() {
    echo >&2 "$@"
    exit 1
}

print_help() {
    echo "Usage: COMMAND [OPTIONS]"
    echo ""
    echo "Commands:"
    echo " --                 Attach terminal to running container"
    echo " l,  logs           Fetch container logs"
    echo " cl, compose-logs   Fetch compose logs"
    echo " u,  update         Update (pull) current image"
    echo
    echo "To get more help with opener, check out our docs at https://github.com/artemkaxboy/docker-opener"
}

take_head() {
    take_head_args=$*
    retval=${take_head_args%%' '*}
}

cut_tail() {
    cut_tail_args=$*
    retval=${cut_tail_args%' '*}
}

take_tail() {
    take_tail_args=$*
    retval=${take_tail_args##*' '}
}

cut_head() {
    cut_head_args=$*
    retval=${cut_head_args#*' '}
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

find_compose_project() {
    ###### find by exact name
    target_compose_project=$(docker ps --filter label=com.docker.compose.project --format '{{.Label "com.docker.compose.project"}}' | grep ^"$1"$ -m1)
    [ -n "$target_compose_project" ] && echo "Found compose with name: $1"

    ###### find by name
    if [ -z "$target_compose_project" ]; then
    target_compose_project=$(docker ps --filter label=com.docker.compose.project --format '{{.Label "com.docker.compose.project"}}' | grep "$1" -m1)
        [ -n "$target_compose_project" ] && echo "Found compose with name containing \`$1\`: $target_compose_project"
    fi

    if [ -z "$target_compose_project" ]; then
        die "Compose not found: $1"
    fi
}

# finds target of search, it may be `cname -f -n 200` or `-f -n 200 cname`
divide_target_and_arguments() {

    args="${*}"

    if [ "${args:0:1}" == "-" ] ; then
        take_tail "$args"
        target=$retval
        cut_tail "$args"
        arguments=$retval
    else
        take_head "$args"
        target=$retval
        cut_head "$args"
        arguments=$retval
    fi
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

    divide_target_and_arguments "$@"
    find_container "$target"
    echo "Fetching logs for $target_id"

    docker logs "$target_id" "$arguments"
}

fetch_compose_logs() {
    [ "$#" -eq 0 ] && die "Target required"

    find_compose_project "$1"
    echo "Fetching logs for compose $target_id"
    shift

    # find all services of the target_compose_project
    compose_services=$(docker ps --all --filter label=com.docker.compose.project="$target_compose_project" --format '{{.Label "com.docker.compose.service"}}:')

    # make fake compose file with all needed services
    # https://stackoverflow.com/a/19347380/1452052
    # replace any of specials ${var//[$'\t\r\n']}
    printf "version: '3.8'\\nservices:\\n  %b\\n    build: ." "${compose_services//[$'\n']/\\n    build: .\\n  }" > /tmp/compose.yml

    # read logs
    docker-compose --project-name "$target_compose_project" --file /tmp/compose.yml logs "$@"
}

update() {
    image=$(docker ps --format "{{.Image}}" | grep artemkaxboy/opener)
    docker pull "$image"
}

##################### START
# stop on any error
# set -e

case $1 in
    h|help|-h|--help)
        print_help ;;
    u|update)
        update ;;
    l|logs)
        shift
        fetch_logs "$@" ;;
    cl|compose-logs)
        shift
        fetch_compose_logs "$@" ;;
    --)
        shift
        connect "$@" ;;
    *)
        connect "$@" ;;
esac
