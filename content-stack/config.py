import boto3

def create_alarm_and_update_code_deploy(alarm_for_code_deploy, alarm_for_lambda, deployment_group_name, application_name, lambda_function_name, aws_region):
    # Create CloudWatch client in specified region
    cloudwatch = boto3.client('cloudwatch', region_name=aws_region)
   
    
    # Create alarms for CodeDeploy and Lambda
    cloudwatch.put_metric_alarm(
        AlarmName=alarm_for_code_deploy,
        AlarmDescription="Alarm for CodeDeploy Deployment Group",
        MetricName="Failed",
        Namespace="AWS/CodeDeploy",
        Statistic="Sum",
        Dimensions=[
            {"Name": "DeploymentGroupName", "Value": deployment_group_name},
            {"Name": "ApplicationName", "Value": application_name}
        ],
        Period=300,
        EvaluationPeriods=1,
        Threshold=1,
        ComparisonOperator="GreaterThanOrEqualToThreshold"
    )
    
    cloudwatch.put_metric_alarm(
        AlarmName=alarm_for_lambda,
        AlarmDescription="Alarm for Lambda Error Rate",
        MetricName="Errors",
        Namespace="AWS/Lambda",
        Statistic="Sum",
        Dimensions=[
            {"Name": "FunctionName", "Value": lambda_function_name}
        ],
        Period=300,
        EvaluationPeriods=1,
        Threshold=1,
        ComparisonOperator="GreaterThanOrEqualToThreshold",
        TreatMissingData="notBreaching"
    )
    
    print(f"CloudWatch Alarms '{alarm_for_code_deploy}' and '{alarm_for_lambda}' have been created in the '{aws_region}' region.")
    
    # Update CodeDeploy deployment group with the new alarm configuration in specified region
    codedeploy = boto3.client('codedeploy', region_name=aws_region)
    codedeploy.update_deployment_group(
        applicationName=application_name,
        currentDeploymentGroupName=deployment_group_name,
        alarmConfiguration={
            'enabled': True,
            'ignorePollAlarmFailure': False,
            'alarms': [
                {'name': alarm_for_code_deploy},
                {'name': alarm_for_lambda}
            ]
        }
    )
    
    print(f"Deployment Group '{deployment_group_name}' updated with the new alarm configuration in the '{aws_region} region.")

# Specify the names for your alarms, application, and deployment group
alarm_for_code_deploy = "your-code-deploy-name"
alarm_for_lambda = "your-alarm-name"
deployment_group_name = "your-deployment-group-name"
application_name = "your-application-name"
lambda_function_name = "your-lambda-function-name"
aws_region = "your-aws-region"

# Create the alarms and update the deployment group in the specified region
create_alarm_and_update_code_deploy(alarm_for_code_deploy, alarm_for_lambda, deployment_group_name, application_name, lambda_function_name, aws_region)
