# GDACK

**Slack Application for Bitcoin trading in [GDAX](https://gdax.com)**

This is a serverless application running in [AWS Lambda](https://aws.amazon.com/lambda/). Using the slash command `/gdack` you make buy, sell, or [HODL](https://www.reddit.com/r/Bitcoin/comments/2b8t78/whats_hodl/) from Slack.

_Disclaimer: I am making this application for myself only. I need an easy way to buy and sell Bitcoins from my phone and GDAX doesn't have a mobile app. You are free to use my code, just beware that I didn't write this as a full 'application'._

## Commands:

- `/gdack account list` - Get all your accounts and amount of funds in them

- `/gdack account history <account_id>` - Get history of specific account. Account ID taken as a parameter

- `/gdack orders list` - List all open orders

- `/gdack orders cancel <order_id>` - Cancel an open order. Order ID taken as a parameter

- `/gdack orders cancel all` - Cancel all open orders

- `/gdack create limit <side> <price> <size>` - Create a Limit order. Parameters are Side (buy or sell), Price per BTC, Size (how many BTC).

- `/gdack create market <side> <size>` - Create a Market order. Parameters are Side (buy or sell), Size (how many BTC).

- `/gdack create stop <side> <price> <size>` - Create a Stop order. Parameters are Side (buy or sell), Price per BTC, Size (how many BTC).

- `/gdack price` - Find current Market price of BTC-USD

- `/gdack status` - Check the status of the GDAX API
