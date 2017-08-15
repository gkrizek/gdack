from gdack.account import Account
from gdack.create import Create
from gdack.orders import Orders
from gdack.price import Price
from gdack.slack import Reply, Comment
from gdack.status import Status
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
            result = Account(
                Text=text,
                Channel=channel_name,
                User=user_name
            )
            message = result
        elif action == "orders":
            result = Orders(
                Text=text,
                Channel=channel_name,
                User=user_name
            )
            message = result
        elif action == "create":
            result = Create(
                Text=text,
                Channel=channel_name,
                User=user_name
            )
            message = result
        elif action == "price":
            result = Price(
                Text=text,
                Channel=channel_name,
                User=user_name
            )
            message = result
        elif action == "status":
            result = Status(
                Text=text,
                Channel=channel_name,
                User=user_name
            )
            message = result
        elif action == "help":
            message = ("Available Commands:\n" +
                       "`/gdack account list`\n" +
                       "`/gdack account history <account_id>`\n" +
                       "`/gdack orders list`\n" +
                       "`/gdack orders cancel <order_id>`\n" +
                       "`/gdack orders cancel all`\n" +
                       "`/gdack create limit <side> <price> <size>`\n" +
                       "`/gdack create market <side> <size>`\n" +
                       "`/gdack create stop <side> <price> <size>`\n" +
                       "`/gdack price`\n" +
                       "`/gdack status`\n" +
                       "`/gdack help`"
                      )
        else:
            message = ("*Error:* Unknown Command.\nAvailable Commands:\n" +
                       "`/gdack account list`\n" +
                       "`/gdack account history <account_id>`\n" +
                       "`/gdack orders list`\n" +
                       "`/gdack orders cancel <order_id>`\n" +
                       "`/gdack orders cancel all`\n" +
                       "`/gdack create limit <side> <price> <size>`\n" +
                       "`/gdack create market <side> <size>`\n" +
                       "`/gdack create stop <side> <price> <size>`\n" +
                       "`/gdack price`\n" +
                       "`/gdack status`\n" +
                       "`/gdack help`"
                      )
        result = Reply(
            ResponseUrl=response_url,
            Message=message
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
