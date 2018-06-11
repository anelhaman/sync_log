#!/bin/sh

for filename in $(pwd)/cluster/*
do
    python logman.py $filename "$(pwd)/logged/" &
done

# use another server
# python logman.py "$(pwd)/cluster/log.txt" "username@remote_host:/logged/"
