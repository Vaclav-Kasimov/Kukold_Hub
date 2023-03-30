from telethon import events
from telethon import TelegramClient
import asyncio
import getpass
import typing



api_id = 20387754
api_hash = 'c47bb9cdd6c140651113f118ae27d79f'
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats='leomatchbot'))
async def msg_handler(event):
    print(event.message.to_dict()['message'])
    await client.log_out()
    client.disconnect()

@client.on(events.NewMessage(chats='schpecc'))
async def msg_handler(event):
    client.disconnect()

def _phone():
    return input('Дай телефон мразота\n')
def get_code():
    return input('Дай код гандон\n')

client.start(phone = _phone, code_callback=get_code)

client.run_until_disconnected()


