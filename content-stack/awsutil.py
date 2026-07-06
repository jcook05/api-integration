import boto3
import os
from botocore.exceptions import ClientError

def getKey(aws_region):
    apigw = boto3.client("apigateway")
    try:
        resp = apigw.get_api_key(
            apiKey=os.environ["key_id"],
            includeValue=True
        )
        return resp["value"]
    except ClientError:
        return getSecureParameter(os.environ["key_name"], aws_region)

""" Method to Get Secure Parameter """
def getSecureParameter(pname, region):
    client = boto3.client('ssm', region_name=region)
    response = client.get_parameter(
    Name=pname,
    WithDecryption=True)
    return response["Parameter"]["Value"]