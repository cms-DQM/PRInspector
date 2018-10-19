#!/bin/bash

if [ "$1" == "-h" ] || [ "$1" == "--help" ];
then
    echo "Runs the app. If -r is added app will be restarted after a crash on first file change. File changes are observed using fswatch."
    exit
fi

if [ "$1" == "-r" ];
then
    while ! { python3 app.py; };
    do
        if [ -x "$(command -v fswatch)" ];
        then
            # Wait for any file to be saved, then restart
            fswatch -1 ./
            echo 'Restarting...'
        else
            break
        fi
    done
else
    python3 app.py;
fi
