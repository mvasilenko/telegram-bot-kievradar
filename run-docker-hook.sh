#!/bin/bash
source .env
nohup ./docker-hook -t $DOCKER_HOOK_TOKEN -c ./deploy.sh &

