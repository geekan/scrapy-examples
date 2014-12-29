#!/bin/sh
set -e

function usage {
    echo "\n  usage:\n      ./startproject.sh <project name>\n"
}

if [ "$1"X == ""X ]; then
    usage
    exit
fi

if [ "$(uname)" == "Darwin" ]; then
    alias sed='sed -i'
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    echo `uname -s`
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    echo `uname -s`
fi

echo "Starting project $1."

cp -r template $1
find $1 -type f | xargs sed -i '' "s/template/$1/"
mv $1/template $1/$1

echo "Create $1 succeed!"
