


def Account(Text, Channel, User):
    text = Text
    try:
        if len(text.split(' ')) == 1:
            message = ("*Error:* sub-command is required.\n" +
                       "Availabe sub-commands:\n" +
                       "`list`\n" +
                       "`history <account_id>`\n"
                      )
        else:
            command = text.split(' ')[1]
            if command == "list":
                message = "this is the list command"
            elif command == "history":
                if len(text.split(' ')) == 2:
                    message = ("*Error:* Account ID is required.\n" +
                               "Example: `/gdack account history abc123`"
                              )
                else:
                    message = "this is the history command"
            elif command == "help":
                message = ("Availabe sub-commands:\n" +
                           "`list`\n" +
                           "`history <account_id>`\n"
                          )
            else:
                message = ("*Error:* Invalid sub-command.\n" +
                           "Availabe sub-commands:\n" +
                           "`list`\n" +
                           "`history <account_id>`\n"
                          )
    except Exception as e:
        print(e)
        message = "*Error:* There was a problem running that command:\n```" + str(e) + "```"

    return message
