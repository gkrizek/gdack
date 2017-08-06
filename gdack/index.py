

def handler(event, context):
    if event:
        return {
            'statusCode': 200,
            'body': str(event)
        }
    else:
        return {
            'statusCode': 400,
            'body': 'Nope'
        }
