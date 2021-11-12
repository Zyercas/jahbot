import logging
from telethon import TelegramClient, events, types
import motor.motor_asyncio
import settings
from random import randint


logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)


client = TelegramClient("jahbot", settings.API_ID, settings.API_HASH).start(
    bot_token=settings.BOT_TOKEN
)
client.parse_mode = "md"


cluster = motor.motor_asyncio.AsyncIOMotorClient()
db = cluster["jahllars"]

async def roller():
    jah = randint(1,2000)
    gek = randint(1,200)
    return({"jah": jah, "gek": gek})

async def sync(users):
    async with await cluster.start_session() as s:
        collection = db["users"]
        for user in users:
            post = {"_id": user, "jah": 0, "gek": 0}
            try:
                await collection.insert_one(post)
            except Exception:
                pass

async def retrieve_coin(user_id):
    async with await cluster.start_session() as s:
        collection = db["users"]
        res = await collection.find_one({"_id": user_id})
        return(res)
    

async def add_coin(coin, user_id):
    async with await cluster.start_session() as s:
        collection = db["users"]
        await collection.update_one({"_id": user_id}, {"$inc": {coin: 1}}, session=s)


@client.on(events.NewMessage(incoming=True))
async def listener(event):
    if event.sender.bot is False and isinstance(event.chat, types.Channel):
        roll = await roller()
        pass
        for coin in roll:
            if coin == "jah" and roll[coin] == 1:
                await add_coin("jah", event.sender_id)
                await event.reply(f"You just found a **Jahllar**! \U0001F4B8")
            elif coin == "gek" and roll[coin] == 1:
                await add_coin("gek", event.sender_id)
                await event.reply(f"You just found a **Gekcoin**! \U0001FA99")


@client.on(events.NewMessage(incoming=True, pattern="/wallet"))
async def fetch_wallet(event):
    res = await retrieve_coin(event.sender_id)
    rep = f"**Jahllars**: {res['jah']} \U0001F4B8\n**Gekcoins**: {res['gek']} \U0001FA99\n\nID: `{event.sender_id}`"
    await event.reply(rep)


@client.on(events.NewMessage(incoming=True, pattern="/sync",from_users=[settings.ADMIN]))
async def fetch_users(event):
    users = await client.get_participants(event.chat_id)
    user_list = []
    for user in users:
        if user.bot is False:
            user_list.append(user.id)
        else:
            pass
    await sync(user_list)
    await event.reply(f"Done!")


@client.on(events.NewMessage(incoming=True, pattern="/help"))
async def help(event):
    res = f"Droprates\n\n0.05% Jahllar\n0.5% Gekcoin\n\n**Probability is rolled for each message.**"
    await event.reply(res)


@client.on(events.NewMessage(incoming=True, pattern="/start"))
async def help(event):
    res = f"Add me to a group to have a chance to win free Jahllars and Gekcoins for every message you type!\n\n/help - How does the bot work?\n/wallet - Receive information about your JahBank wallet."
    await event.reply(res)


def main():
    client.start()
    print("Bot on!")
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
