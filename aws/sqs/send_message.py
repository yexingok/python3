#!/usr/bin/python

import boto3
from time import localtime, strftime

now = strftime("%Y-%m-%d %H:%M:%S", localtime())
message = "Hello World from Yexing - message created at: {}".format(now)
messageattrib = {
    'Author': {
        'DataType':'String',
        'StringValue':'Yexing'
    },
    'Time': {
        'DataType':'String',
        'StringValue':now
    }
}
print "Send Message: \n" + message

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='backbone-test')
response = queue.send_message(MessageBody=message, MessageAttributes=messageattrib)

print "\nMessage ID: {}\t Message MD5: {}".format(response.get('MessageId'),response.get('MD5OfMessageBody'))
