#!/usr/bin/env bash

# This scripy will try to read environment variables,
# push docker image from local machine to the AWS ECR registry
# and deploy service to the ECS cluster.
# Written to be run by Circle CI

: "${CIRCLE_PROJECT_REPONAME:?The environment variable CIRCLE_PROJECT_REPONAME needs to be set}"


# more bash-friendly output for jq
JQ="jq --raw-output --exit-status"

# check if AWS region is set
if [ -z ${AWS_DEFAULT_REGION} ]; then AWS_DEFAULT_REGION=us-east-1; fi

configure_aws_cli(){
    aws --version
    aws configure set default.region ${AWS_DEFAULT_REGION}
    aws configure set default.output json
}

deploy_cluster() {

    family="$CIRCLE_PROJECT_REPONAME-task-family"

    make_task_def
    register_definition
    echo aws ecs update-service --cluster $CIRCLE_PROJECT_REPONAME --service $CIRCLE_PROJECT_REPONAME-service --task-definition $revision
    if [[ $(aws ecs update-service --cluster $CIRCLE_PROJECT_REPONAME --service $CIRCLE_PROJECT_REPONAME-service --task-definition $revision | \
                   $JQ '.service.taskDefinition') != $revision ]]; then
        echo "Error updating service."
        return 1
    fi

    # wait for older revisions to disappear
    # not really necessary, but nice for demos
    for attempt in {1..30}; do
        if stale=$(aws ecs describe-services --cluster $CIRCLE_PROJECT_REPONAME --services $CIRCLE_PROJECT_REPONAME-service | \
                       $JQ ".services[0].deployments | .[] | select(.taskDefinition != \"$revision\") | .taskDefinition"); then
            echo "Waiting for stale deployments:"
            echo "$stale"
            sleep 5
        else
            echo "Deployed!"
            return 0
        fi
    done
    echo "Service update took too long."
    return 1
}

make_task_def(){
    task_template='[
        {
            "name": "%s",
            "image": "%s.dkr.ecr.%s.amazonaws.com/%s:%s",
            "essential": true,
            "memory": 200,
            "cpu": 10,
            "portMappings": [
                {
                    "containerPort": 8080,
                    "hostPort": 80
                }
            ],
            "environment" : [
                { "name" : "TOKEN_BOT", "value" : "%s" }
            ]

        }
    ]'

    task_def=$(printf "$task_template" $CIRCLE_PROJECT_REPONAME $AWS_ACCOUNT_ID $AWS_DEFAULT_REGION $CIRCLE_PROJECT_REPONAME $CIRCLE_SHA1 $TOKEN_BOT)
    echo $task_def
}

push_ecr_image(){
    eval $(aws ecr get-login --region eu-central-1)
    docker push $AWS_ACCOUNT_ID.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/$CIRCLE_PROJECT_REPONAME:$CIRCLE_SHA1
}

register_definition() {

    if revision=$(aws ecs register-task-definition --container-definitions "$task_def" --family $family | $JQ '.taskDefinition.taskDefinitionArn'); then
        echo "Revision: $revision"
    else
        echo "Failed to register task definition"
        return 1
    fi

}

configure_aws_cli
push_ecr_image
deploy_cluster
