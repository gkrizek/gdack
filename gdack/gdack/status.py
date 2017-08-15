

def Status(Text, Channel, User):
    try:
        message = "<https://status.gdax.com|GDAX Staus>"
    except Exception as e:
        print(e)
        message = "*Error:* There was a problem running that command:\n```" + str(e) + "```"
    return message
