#! /bin/bash
IMAGE="mvasilenko/telegram-bot-kievradar"
docker ps | grep $IMAGE | awk '{print $1}' | xargs docker stop
docker pull $IMAGE
docker run -d --env-file ~/telegram-bot-kievradar/.env $IMAGE
