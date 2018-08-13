#!/usr/bin/python

import boto3

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='backbone-test')

for message in queue.receive_messages(MessageAttributeNames=['Author'], WaitTimeSeconds=20, MaxNumberOfMessages=10):
    author_text = ''
    if message.message_attributes is not None:
        author_name = message.message_attributes.get('Author').get('StringValue')
        if author_name:
            author_text = ' \nSent from ({0})'.format(author_name)
        print "Message received:\n{0} {1}".format(message.body, author_text)
        print
        message.delete()
