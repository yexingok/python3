#!/bin/bash

# How to setup https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/RunLambdaSchedule.html
# Refer AWS Cron: https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
# Below schedule will run at 23:03 CST.

rule=$(aws events put-rule \
    --profile jp \
    --region us-east-1 \
    --name pubmed-ftptos3daily \
    --schedule-expression 'cron(3 15 * * ? *)')

aws lambda add-permission \
    --profile jp \
    --region us-east-1 \
    --function-name pubmed-updateftptos3 \
    --statement-id my-scheduled-event \
    --action 'lambda:invokefunction' \
    --principal events.amazonaws.com \
    --source-arn $rule

aws events put-targets \
    --profile jp \
    --region us-east-1 \
    --rule pubmed-ftptos3daily \
    --targets file://targets.json
