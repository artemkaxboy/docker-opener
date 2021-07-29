#!/bin/sh

set -e

echo "" > command.sh
chmod 755 command.sh
python/make_command.py "$@"
./command.sh
