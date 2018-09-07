#!/bin/bash

rm -f wechat.zip
tmpdir=$(mktemp -d /tmp/lambda-XXXXX)
zipfile=${tmpdir}/wechat.zip

virtualenv=${tmpdir}/virtual-env
(
    python3 -mvenv $virtualenv
    source $virtualenv/bin/activate
    pip install requests
)

rsync -va main.py iciba.py wechat.json $tmpdir/
(cd $tmpdir; zip -r9 $zipfile *.py wechat.json)
(cd $virtualenv/lib/python3*/site-packages/; zip -gr9 $zipfile *)
mv $zipfile ./

# Delete previous function so we can re-deploy
# aws lambda delete-function \
#    --profile yx \
#    --region us-west-2 \
#    --function-name wechat-iciba-everyday

aws lambda create-function \
    --profile yx \
    --region us-west-2 \
    --function-name wechat-iciba-everyday \
    --zip-file fileb://wechat.zip \
    --role arn:aws:iam::12345:role/CloudWatchFullAccess \
    --handler main.main \
    --runtime python3.6 \
    --timeout 120 \
    --memory-size 512
