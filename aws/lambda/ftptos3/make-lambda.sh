#!/bin/bash


zip -9 ftptos3.zip ftptos3.py

aws lambda delete-function \
    --profile sgp \
    --region us-east-1 \
    --function-name pubmed-updateftptos3

aws lambda create-function \
    --profile sgp \
    --region us-east-1 \
    --function-name pubmed-updateftptos3 \
    --zip-file fileb://ftptos3.zip \
    --role arn:aws:iam::123456:role/AllowLambdaAccessS3 \
    --handler ftptos3.main \
    --runtime python3.6 \
    --timeout 120 \
    --memory-size 1024
