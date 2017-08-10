#!/usr/bin/python
#
# Author: Graham Krizek
#
# Description:
#    Create infrastructure for GDACK
#
#
#

import sys
import troposphere.apigateway as api
from troposphere import GetAtt, Join, Parameter, Ref, Template, Tags, Output
from troposphere.iam import Role, Policy
from troposphere.awslambda import Function, Code, Environment, Permission
from troposphere.route53 import RecordSetType, AliasTarget
from troposphere.s3 import Bucket, VersioningConfiguration
from troposphere.events import Rule, Target
from troposphere.sns import Topic, Subscription

t = Template()
t.add_version("2010-09-09")
t.add_description("GDACK Infrastructure")

# Parameters

lambdaKey = t.add_parameter(Parameter(
    "lambdaKey",
    Description="S3 Key for Lambda Function Zip",
    Type="String"
))

lambdaBucket = t.add_parameter(Parameter(
    "lambdaBucket",
    Description="S3 Bucket for Lambda Function Zip",
    Default="gdack",
    Type="String"
))

# Resources

lambdaRole = t.add_resource(Role(
    "LambdaRole",
    Path="/",
    RoleName="GDACK-LambdaRole",
    Policies=[
        Policy(
            PolicyName="GDACK-LambdaPolicy-Logs",
            PolicyDocument={
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": [
                        "logs:*"
                    ],
                    "Resource": "arn:aws:logs:*:*:*",
                    "Effect": "Allow"
                }]
            }
        ),
        Policy(
            PolicyName="GDACK-LambdaPolicy-SSM",
            PolicyDocument={
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": [
                        "ssm:Get*"
                    ],
                    "Resource": "*",
                    "Effect": "Allow"
                }]
            }
        )
    ],
    AssumeRolePolicyDocument={
        "Version": "2012-10-17",
        "Statement": [{
            "Action": ["sts:AssumeRole"],
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "lambda.amazonaws.com"
                ]
            }
        }]
    },
))

apiRole = t.add_resource(Role(
    "ApiRole",
    Path="/",
    RoleName="GDACK-ApiRole",
    Policies=[Policy(
        PolicyName="GDACK-ApiPolicy",
        PolicyDocument={
            "Version": "2012-10-17",
            "Statement": [{
                "Action": [
                    "logs:*",
                    "lambda:Invoke*",
                    "iam:PassRole",
                    "cloudwatch:*"
                ],
                "Resource": "*",
                "Effect": "Allow"
            }]
        })],
    AssumeRolePolicyDocument={
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "lambda.amazonaws.com",
                    "apigateway.amazonaws.com"
                ]
            }
        }]
    },
))

lambdaFunction = t.add_resource(Function(
    "lambdaFunction",
    FunctionName="GDACK",
    Code=Code(
        S3Bucket=Ref(lambdaBucket),
        S3Key=Ref(lambdaKey)
    ),
    Description="GDACK Function",
    Handler="index.handler",
    Role=GetAtt(lambdaRole, "Arn"),
    Runtime="python3.6",
    MemorySize=128,
    Timeout="180"
))

restApi = t.add_resource(api.RestApi(
    "restApi",
    Name="GDACK"
))

apiResource = t.add_resource(api.Resource(
    "apiResource",
    RestApiId=Ref(restApi),
    PathPart="{proxy+}",
    ParentId=GetAtt(restApi, "RootResourceId"),
))

apiMethod = t.add_resource(api.Method(
    "apiMethod",
    DependsOn='lambdaFunction',
    RestApiId=Ref(restApi),
    AuthorizationType="NONE",
    ResourceId=Ref(apiResource),
    HttpMethod="ANY",
    Integration=api.Integration(
        Credentials=GetAtt(apiRole, "Arn"),
        Type="AWS_PROXY",
        IntegrationHttpMethod='ANY',
        Uri=Join("", [
            "arn:aws:apigateway:us-west-2:lambda:path/2015-03-31/functions/",
            GetAtt(lambdaFunction, "Arn"),
            "/invocations"
        ])
    )
))

stageName = "v1"

apiDeployment = t.add_resource(api.Deployment(
    "apiDeployment",
    DependsOn="apiMethod",
    RestApiId=Ref(restApi),
))

apiStage = t.add_resource(api.Stage(
    "apiStage",
    StageName=stageName,
    RestApiId=Ref(restApi),
    DeploymentId=Ref(apiDeployment)
))

apiKey = t.add_resource(api.ApiKey(
    "apiKey",
    StageKeys=[api.StageKey(
        RestApiId=Ref(restApi),
        StageName=Ref(apiStage)
    )]
))

snsTopic = t.add_resource(Topic(
    "snsTopic",
    DisplayName="GDACK",
    TopicName="GDACK",
    Subscription=[
        Subscription(
            Endpoint=GetAtt(lambdaFunction, "Arn"),
            Protocol="lambda"
        )
    ]
))

ApiPermission = t.add_resource(Permission(
    "ApiPermission",
    FunctionName=Ref(lambdaFunction),
    Action="lambda:InvokeFunction",
    Principal="apigateway.amazonaws.com",
    SourceArn=Join("", ["arn:aws:execute-api:us-west-2:", Ref("AWS::AccountId"), ":", Ref(restApi), "/*/*/*"])
))

# Output

WebhookUrl = t.add_output(Output(
    "WebhookUrl",
    Description="URL for Slack Endpoint",
    Value=Join("", [Ref(restApi), ".execute-api.", Ref("AWS::Region"), ".amazonaws.com/", stageName, "/slack"])
))

j = t.to_json()

with open('gdack.template', 'w') as fd:
    fd.write(j)

print("export complete")
