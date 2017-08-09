import boto3
from gdack import Router

def handler(event, context):

    if event:
        print("Event Data:\n" + str(event))
        # Get Secrets from SSM
        ssm = boto3.client('ssm')
        env = 'prod'
        response = ssm.get_parameters_by_path(
            Path='/gdack/' + env,
            WithDecryption=True
        )
        for index, value in enumerate(response['Parameters']):
            name = value['Name'].split('/')[-1]
            os.environ[name] = value['Value']

        try:
            result = Router(
                headers=event['headers'],
                body=event['body']
            )
            return {
                'statusCode': 200,
                'body': result
            }
        except KeyError:
            return {
                'statusCode': 400,
                'body': 'Bad Request'
            }

    else:
        return {
            'statusCode': 400,
            'body': 'No Event Found'
        }
