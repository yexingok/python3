#!/bin/bash

# How to setup https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/RunLambdaSchedule.html
# Refer AWS Cron: https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
# Below schedule will run at 08:15 CST.

rule=$(aws events put-rule \
    --profile yx \
    --region us-west-2 \
    --name wechat-iciba-everyday \
    --schedule-expression 'cron(15 0 * * ? *)')

aws lambda add-permission \
    --profile yx \
    --region us-west-2 \
    --function-name wechat-iciba-everyday \
    --statement-id my-scheduled-event \
    --action 'lambda:invokefunction' \
    --principal events.amazonaws.com \
    --source-arn $rule

aws events put-targets \
    --profile yx \
    --region us-west-2 \
    --rule wechat-iciba-everyday \
    --targets file://targets.json
