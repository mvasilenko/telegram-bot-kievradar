#! /bin/bash
IMAGE="mvasilenko/telegram-bot-kievradar"
DIR=`pwd`
docker pull $IMAGE
docker ps | grep $IMAGE | awk '{print $1}' | xargs docker stop
docker run -d --rm --env-file $DIR/.env $IMAGE
docker rmi $(docker images --filter "dangling=true" -q --no-trunc) 2>/dev/null
