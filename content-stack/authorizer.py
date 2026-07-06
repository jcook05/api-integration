import awsutil
import json

def lambda_authorizer(event, context):
    print(event)
    # Retrieve request parameters from the Lambda function input:
    headers = event['headers']
    print(headers)

    # Parse the input for the parameter values
    tmp = event['methodArn'].split(':')
    apiGatewayArnTmp = tmp[5].split('/')
    awsAccountId = tmp[4]
    region = tmp[3]
    restApiId = apiGatewayArnTmp[0]
    stage = apiGatewayArnTmp[1]
    method = apiGatewayArnTmp[2]
    resource = '/'
    
    if (apiGatewayArnTmp[3]):
       resource += apiGatewayArnTmp[3]
    
    # Perform authorization to return the Allow policy for correct parameters and the 'Unauthorized' error, otherwise.  
    authResponse = {}
    condition = {}
    condition['IpAddress'] = {}
    basicauth = False
    username, password = decodeAuth(headers['Authorization'])
    epw = awsutil.getSecureParameter('your/pw/path', 'your-region')

    if username == 'your-username' and password == epw:
        basicauth = True 
    print(basicauth)
    api_key = awsutil.getKey()
    
    if headers['x-api-key'] == api_key and basicauth == True:
        response = generateAllow('me', event['methodArn'])
        print('authorized')
        return json.loads(response)
    else:
        print('unauthorized')
        raise Exception('Unauthorized') # Return a 401 Unauthorized response
        #return 'unauthorized'
   
def decodeAuth(auth_header):
    # Check if the authorization header is present and starts with "Basic "
    if auth_header and auth_header.startswith("Basic "):
        # Extract encoded credentials (you can decide how to encode them)
        encoded_credentials = auth_header.split(" ")[1]
        # Decode the encoded credentials
        decoded_credentials = f"decode {encoded_credentials}"
        # Split the decoded credentials into username and password
        username, password = decoded_credentials.split(":", 1)
        return username, password
    else:
        return None, None

def generatePolicy(principalId, effect, resource):
        authResponse = {}
        authResponse['principalId'] = principalId
        if (effect and resource):
            policyDocument = {}
            policyDocument['Version'] = '2012-10-17'
            policyDocument['Statement'] = [];
            statementOne = {}
            statementOne['Action'] = 'execute-api:Invoke'
            statementOne['Effect'] = effect
            statementOne['Resource'] = resource
            policyDocument['Statement'] = [statementOne]
            authResponse['policyDocument'] = policyDocument
        
        authResponse['context'] = {
            "stringKey": "stringval",
            "numberKey": 123,
            "booleanKey": True
        }
        
        authResponse_JSON = json.dumps(authResponse)

        return authResponse_JSON
        
def generateAllow(principalId, resource):
    return generatePolicy(principalId, 'Allow', resource)

def generateDeny(principalId, resource):
    return generatePolicy(principalId, 'Deny', resource)