import boto3
import json

def InvokeSelf(body):
    awslambda = boto3.client('lambda')

    obj = {
        'headers': {
            'gdack-manual-invocation': 'true'
        },
        'body': body
    }

    result = awslambda.invoke(
        FunctionName="GDACK",
        InvocationType="Event",
        Payload=json.dumps(obj)
    )
    return result['StatusCode']
