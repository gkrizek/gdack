from gdack.slack import Reply, Comment
from gdack.utils import InvokeSelf
from urllib.parse import parse_qs
import json
import os


def Router(headers, body):
    # Check if this is a manual invocation
    if 'gdack-manual-invocation' in headers:
        channel_id = body['channel_id'][0]
        channel_name = body['channel_name'][0]
        user_id = body['user_id'][0]
        user_name = body['user_name'][0]
        text = body['text'][0]
        action = text.split(' ')[0]
        response_url = body['response_url'][0]

        if action == 'account':
            result = Reply(
                ResponseUrl=response_url,
                Message="account"
            )
            print(result)
        elif action == 'orders':
            result = Reply(
                ResponseUrl=response_url,
                Message="orders"
            )
            print(result)
        elif action == 'create':
            result = Reply(
                ResponseUrl=response_url,
                Message="create"
            )
            print(result)
        elif action == 'price':
            result = Reply(
                ResponseUrl=response_url,
                Message="price"
            )
            print(result)
        elif action == 'status':
            result = Reply(
                ResponseUrl=response_url,
                Message="status"
            )
            print(status)
        else:
            result = Reply(
                ResponseUrl=response_url,
                Message="Unknown"
            )
            print(result)
        return

    else:
        body = parse_qs(body)
        token = body['token'][0]
        if token == os.environ["SLACK_VERIFY_TOKEN"]:
            try:
                result = InvokeSelf(
                    body=body
                )
                return "Command Received..."
            except Exception as e:
                print(e)
                return "There was a problem executing command:\n```" + str(e) + "```"
        else:
            return "Unauthorized"
