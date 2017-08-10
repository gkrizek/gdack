from slackclient import SlackClient
import requests
import json
import os


def Comment(Channel, Message, *args, **kwargs):

    slack_token = os.environ["SLACK_API_TOKEN"]
    sc = SlackClient(slack_token)

    try:
        # Can optionally pass in an Attachment for Interactive Buttons
        if 'Attachments' in kwargs:
            result = sc.api_call(
                "chat.postMessage",
                channel=Channel,
                link_names=1,
                text=Message,
                attachments=kwargs['Attachments']
            )
        else:
            result = sc.api_call(
                "chat.postMessage",
                channel=Channel,
                link_names=1,
                text=Message
            )
        if not result['ok']:
            print(result)
            return "Comment Failed"
        else:
            return "Comment Successful"

    except Exception as e:
        print(e)
        return "Error on Comment"


def Reply(ResponseUrl, Message, *args, **kwargs):

    try:
        # Can optionally pass in an Attachment for Interactive Buttons
        if 'Attachments' in kwargs:
            data = {
                'text': Message,
                'attachments': kwargs['Attachments']
            }
        else:
            data = {
                'text': Message
            }
        r = requests.post(ResponseUrl, json=data)
        if r.text != 'ok':
            print(r)
            return "Comment Failed"
        else:
            return "Comment Successful"

    except Exception as e:
        print(e)
        return "Error on Comment"
