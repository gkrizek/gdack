import boto3

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

        return {
            'statusCode': 200,
            'body': str(event)
        }
    else:
        return {
            'statusCode': 400,
            'body': 'Nope'
        }
