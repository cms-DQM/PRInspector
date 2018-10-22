#!/bin/bash

if [ "$1" == "-h" ] || [ "$1" == "--help" ];
then
    echo "Runs the app. If -r is added app will be restarted after a crash on first file change. File changes are observed using fswatch. If -d is added, app will launch in debug mode."
    exit
fi

for arg; do
    case $arg in
        -r)
        AUTO_RELOAD="true"
        ;;
        -d)
        DEBUG="-d"
        ;;
    esac
done

CMD="python3 app.py $DEBUG"

if [[ $AUTO_RELOAD == "true" ]];
then
    while ! { $CMD; };
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
    $CMD;
fi
