import re


def Create(Text, Channel, User):
    text = Text
    try:
        if len(text.split(' ')) == 1:
            message = ("*Error:* sub-command is required.\n" +
                       "Availabe sub-commands:\n" +
                       "`limit <side> <price> <size>`\n" +
                       "`market <side> <size>`\n" +
                       "`stop <side> <price> <size>`"
                      )
        else:
            command = text.split(' ')[1]
            if command == "limit":
                if len(text.split(' ')) < 5:
                    message = ("*Error:* Side, Price, and Size are required.\n" +
                               "Example:\n" +
                               "`/gdack create limit buy 2500.00 0.125`"
                              )
                else:
                    side = text.split(' ')[2]
                    price = text.split(' ')[3]
                    size = text.split(' ')[4]
                    if side not in ['buy', 'sell']:
                        return "*Error:* Side is not one of `buy` or `sell`"
                    isMoney = re.match(r'^\d{1,9}\.\d\d$', price)
                    if not isMoney:
                        return "*Error:* Price must be in format of: 2500.00"

                    message = "this is a create limit command"

            elif command == "market":
                if len(text.split(' ')) < 4:
                    message = ("*Error:* Side and Size are required.\n" +
                               "Example:\n" +
                               "`/gdack create market buy 0.125`"
                              )
                else:
                    side = text.split(' ')[2]
                    size = text.split(' ')[4]
                    if side not in ['buy', 'sell']:
                        return "*Error:* Side is not one of `buy` or `sell`"

                    message = "this is a create market command"

            elif command == "stop":
                if len(text.split(' ')) < 5:
                    message = ("*Error:* Side, Price, and Size are required.\n" +
                               "Example:\n" +
                               "`/gdack create stop buy 2500.00 0.125`"
                              )
                else:
                    side = text.split(' ')[2]
                    price = text.split(' ')[3]
                    size = text.split(' ')[4]
                    if side not in ['buy', 'sell']:
                        return "*Error:* Side is not one of `buy` or `sell`"
                    isMoney = re.match(r'^\d{1,9}\.\d\d$', price)
                    if not isMoney:
                        return "*Error:* Price must be in format of: 2500.00"

                    message = "this is a create stop command"

            elif command == "help":
                message = ("Availabe sub-commands:\n" +
                           "`limit <side> <price> <size>`\n" +
                           "`market <side> <size>`\n" +
                           "`stop <side> <price> <size>`"
                          )
            else:
                message = ("*Error:* Invalid sub-command.\n" +
                           "Availabe sub-commands:\n" +
                           "`limit <side> <price> <size>`\n" +
                           "`market <side> <size>`\n" +
                           "`stop <side> <price> <size>`"
                          )
    except Exception as e:
        print(e)
        message = "*Error:* There was a problem running that command:\n```" + str(e) + "```"

    return message
