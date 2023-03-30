from telethon import events
from telethon import TelegramClient
import asyncio
import getpass
import typing



api_id = 20387754
api_hash = 'c47bb9cdd6c140651113f118ae27d79f'
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats='schpecc'))
async def msg_handler(event):
    print(event.message.to_dict()['message'])
    await client.log_out()
    client.disconnect()

# async def login():

#     await client.sign_in(phone)  # send code
#
#     code = input('enter code: ')
#     await client.sign_in(phone, code)
# asyncio.run(login())
_phone = '+447960619415'


def get_code():
    return input('kod dai sujka: ')
client.start(phone = _phone, code_callback=get_code)

client.run_until_disconnected()


