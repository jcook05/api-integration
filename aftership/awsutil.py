import boto3
import os
from botocore.exceptions import ClientError

def getKey():
    apigw = boto3.client("apigateway")
    try:
        resp = apigw.get_api_key(
            apiKey=os.environ["key_id"],
            includeValue=True
        )
        return resp["value"]
    except ClientError:
        ssm = boto3.client("ssm")
        param = ssm.get_parameter(
            Name=os.environ["key_name"],
            WithDecryption=True
        )
        return param["Parameter"]["Value"]
