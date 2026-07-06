import hmac 
import base64
import hashlib
import traceback
import awsutil
import json

def verify_signature(payload, signature, secret_key):
    """
    Verify the signature of an Aftership webhook.

    Args:
    - payload (str): The payload of the webhook.
    - signature (str): The signature included in the webhook headers.
    - secret_key (str): The secret key used to generate the signature.

    Returns:
    - bool: True if the signature is valid, False otherwise.
    """
    print(type(payload))
    print(type(signature))
    print(type(secret_key))
    expected_signature = base64.b64encode(
        hmac.new(
            secret_key.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
        ).digest()
    ).decode()
    result = hmac.compare_digest(signature, expected_signature)
    if not result:
        print(signature, expected_signature)
    return result

""" Lambda Authorizer """
def lambda_authorizer(event, context):
    try:
        print(event)
        # Retrieve request parameters from the Lambda function input:
        headers = event["headers"]
        print(headers)

        # Parse the input for the parameter values
        tmp = event["methodArn"].split(":")
        apiGatewayArnTmp = tmp[5].split("/")
        awsAccountId = tmp[4]
        region = tmp[3]
        restApiId = apiGatewayArnTmp[0]
        stage = apiGatewayArnTmp[1]
        method = apiGatewayArnTmp[2]
        resource = "/"

        if apiGatewayArnTmp[3]:
            resource += apiGatewayArnTmp[3]

        # Perform authorization to return the Allow policy for correct parameters and the 'Unauthorized' error, otherwise.
        condition = {}
        condition["IpAddress"] = {}

        api_key = awsutil.getKey()

        if headers["X-Api-Key"] == api_key:
            response = generateAllow("me", event["methodArn"])
            print("authorized")
            return json.loads(response)
        else:
            print("unauthorized")
            # Return a 401 Unauthorized response
            raise Exception("Unauthorized")
    except Exception as error:
        print("An exception occurred:", error)
        traceback.print_exc()

""" Method to generate IAM policy authorizing use of API Gateway """
def generatePolicy(principalId, effect, resource):
    authResponse = {}
    authResponse["principalId"] = principalId
    if effect and resource:
        policyDocument = {}
        policyDocument["Version"] = "2012-10-17"
        policyDocument["Statement"] = []
        statementOne = {}
        statementOne["Action"] = "execute-api:Invoke"
        statementOne["Effect"] = effect
        statementOne["Resource"] = resource
        policyDocument["Statement"] = [statementOne]
        authResponse["policyDocument"] = policyDocument

    authResponse["context"] = {
        "stringKey": "stringval",
        "numberKey": 123,
        "booleanKey": True,
    }

    authResponse_JSON = json.dumps(authResponse)
    return authResponse_JSON

def generateAllow(principalId, resource):
    return generatePolicy(principalId, "Allow", resource)

def generateDeny(principalId, resource):
    return generatePolicy(principalId, "Deny", resource)
