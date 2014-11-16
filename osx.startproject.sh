#!/bin/sh
set -e

function usage {
    echo "\n  usage:\n      ./startproject.sh <project name>\n"
}

if [ "$1" == "" ]; then
    usage
    exit
fi

echo "starting project $1..."
cp -r template $1
find ./test -type f | xargs sed -i '' 's/template/test/' 


