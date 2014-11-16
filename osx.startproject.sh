#!/bin/sh
set -e

function usage {
    echo "\n  usage:\n      ./startproject.sh <project name>\n"
}

if [ "$1" == "" ]; then
    usage
    exit
fi

echo "Starting project $1."

cp -r template $1
find ./test -type f | xargs sed -i '' "s/template/$1/"
mv $1/template $1/$1

echo "Create $1 succeed!"
