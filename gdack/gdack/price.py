import gdax

def Price(Text, Channel, User):
    try:

        auth_client = gdax.AuthenticatedClient(
                        key,
                        b64secret,
                        passphrase,
                        api_url="https://api-public.sandbox.gdax.com",
                        product_id="BTC-USD"
                    )
        message = "this is the price command"
    except Exception as e:
        print(e)
        message = "*Error:* There was a problem running that command:\n```" + str(e) + "```"
    return message
