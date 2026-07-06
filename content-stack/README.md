# Content Stack Webhook Integration

This API Gateway enabled Lambda Function, implemented via the Serverless Framework has been developed to allow for the publishing of Content Stack actions to an SNS Topic.

## API Key
Store key name in SSM Parameter store.
The key can be acquired via the AWS Console or CLI:  

`aws ssm get-parameter --name path/to/key/name --with-decryption`

## Infrastructure Setup
SNS Topic must exist

## Serverless Framework: 
Installation: 
https://www.serverless.com/framework/docs/getting-started/

AWS Docs:
https://www.serverless.com/framework/docs/providers/aws/

## To Deploy:

Setup: Install Serverless Framework
1. run ```sls package```
2. review generated CloudFormation templates in the .serverless folder
3. run ```sls deploy```

## Test Locally

To test locally use a test event json file. Generate a test json file based on Content Stack Data Formats 
here:  https://www.contentstack.com/docs/headless-cms/webhook-data-format

`serverless invoke local --function contentstack --path test/publish.json`
`serverless invoke local --function authorizer --path test/basicauth.json`

## Test via Lambda
Add the publish.json into a test event on Lambda.  

aws lambda invoke --function-name content-stack-dev-contentstack \
 --cli-binary-format raw-in-base64-out \
 --payload file://test/basicauth.json \
 --region <your-region> response.json

## Usage 
`
Get the key:  `the-key = aws ssm get-parameter --name /your/api/key --with-decryption`

Call with x-api-key in the Header: 
    Include Header:  -H "x-api-key: the-key"