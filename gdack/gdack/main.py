from gdack.utils import InvokeSelf
from urllib.parse import parse_qs
import json
import os


def Router(headers, body):
    # Check if this is a manual invocation
    if 'gdack-manual-invocation' in headers:
        return 'ok'
    else:
        body = parse_qs(body)
        token = body['token'][0]
        print(token)
        print(body)
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
