#!/bin/bash

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
