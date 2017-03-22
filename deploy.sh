#! /bin/bash
IMAGE="mvasilenko/telegram-bot-kievradar"
DIR=`pwd`
docker ps | grep $IMAGE | awk '{print $1}' | xargs docker stop
docker pull $IMAGE
docker run --rm -d --env-file $DIR/.env $IMAGE
