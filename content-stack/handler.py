import json
import boto3
from botocore.client import Config
import os
import notification

def contentstack(event, context):
    try:
        print(event)
        body = event["body"]
        print(type(body))
        if type(body) is str:
            body = json.loads(body)
        print(body)
        for k in body:
            print(k)
        data = body["data"]
        entry = data["entry"]["title"]
        ctype = data["content_type"]["title"]
        environment = data["environment"]["name"]
        emailSubject = "Contentstack Webhook - " + entry + " Published in " + environment 
        client = boto3.client('sns', config=Config(region_name='your-aws-region'))
        response = client.publish(
        TopicArn=os.environ["topicarn"] ,
        Message=json.dumps(body),
        Subject=emailSubject, 
        )
        notification.slackNotify(entry, ctype, environment, "Published")
        body = {
            "message": "Message Received"
        }
        response = {"statusCode": 200, "body": json.dumps(body)}
        return response
    except:
        body = {
            "message": "Server Error"
        }
        response = {"statusCode": 502, "body": json.dumps(body)}
        return response