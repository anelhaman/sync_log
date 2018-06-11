#!/bin/sh

python logman.py "$(pwd)/cluster/log.txt" "$(pwd)/logged/"

# use another server
# python logman.py "$(pwd)/cluster/log.txt" "username@remote_host:/logged/"
