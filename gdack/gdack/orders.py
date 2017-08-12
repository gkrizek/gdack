

def Orders(Text, Channel, User):
    text = Text
    try:
        if len(text.split(' ')) == 1:
            message = ("*Error:* sub-command is required.\n" +
                       "Availabe sub-commands:\n" +
                       "`list`\n" +
                       "`cancel <order_id>`\n" +
                       "`cancel all`"
                      )
        else:
            command = text.split(' ')[1]
            if command == "list":
                message = "this is the list command"
            elif command == "cancel":
                if len(text.split(' ')) == 2:
                    message = ("*Error:* Order ID is required.\n" +
                               "Example: `/gdack orders cancel abc123`"
                              )
                else:
                    if text.split(' ')[2] == 'all':
                        message = "this is the order cancel all command"
                    else:
                        message = "this is the order cancel id command"
            elif command == "help":
                message = ("Availabe sub-commands:\n" +
                           "`list`\n" +
                           "`cancel <order_id>`\n" +
                           "`cancel all`"
                          )
            else:
                message = ("*Error:* Invalid sub-command.\n" +
                           "Availabe sub-commands:\n" +
                           "`list`\n" +
                           "`cancel <order_id>`\n" +
                           "`cancel all`"
                          )
    except Exception as e:
        print(e)
        message = "*Error:* There was a problem running that command:\n```" + str(e) + "```"

    return message
