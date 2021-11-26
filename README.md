
# JahBot

JahBot is a Telegram bot written in Python 3.9 using the [Telethon](https://github.com/LonamiWebs/Telethon) library and [Motor](https://github.com/mongodb/motor).
I coded this bot to practice what I learned about MongoDB and because of a silly joke one of my friends made (the joke being: [this](https://preview.redd.it/hl68bbom1ei21.jpg?auto=webp&s=28713fa6eca92ff5d1280b46dac7d31748c8811f)). 

The bot works by triggering every time a message is sent on a group: currently the odds of dropping a jahllar are 1/2000 and 1/200 for gekcoins.

The coins are completely useless: it's just meant to be a funny joke.
## Installation & Deployment

First, make sure to install all of the dependencies:

```bash
  pip3 install -r requirements.txt
```
Then, the bot requires a MongoDB instance to connect to. The bot defaults to a local instance, editing it to support a remote one should be easy enough (refer to Motor's docs).

Once the instance is up, message @BotFather on Telegram and create a bot. Once you have the API Token (it'll look something like this: 1234567890:AABCDEFGHK_JLMN) open the settings.py file and fill the BOT_TOKEN variable with it.

You'll need to provide your own API ID/HASH pair. You can get those from https://my.telegram.org/auth.

Lastly, provide the ID of your own Telegram account. You can get it from @getidsbot on Telegram.

Once everything is filled, start the bot with:

```bash
  python3 main.py
```

If the message "Bot on!" appears, you've done everything correctly.