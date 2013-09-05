#!/bin/bash
base_url="http://${1}/"
echo "does it work?"
echo "raw:"
#curl --silent "$base_url"
result=`curl --silent "$base_url"`

echo "result:"

if [ "$result" == "Hello World!" ]
then
    echo "works!"
    exit 0;
fi

echo "failed :("
exit 1
