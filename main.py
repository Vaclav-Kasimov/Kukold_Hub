from telethon import events
from telethon import TelegramClient
import time
import re

api_id = 20387754
api_hash = 'c47bb9cdd6c140651113f118ae27d79f'
vinchik = 'leomatchbot'
client = TelegramClient('session_name', api_id, api_hash)
cities = input('Введи города через пробел с запятой').split(', ')

@client.on(events.NewMessage(chats=vinchik, incoming=True))
async def msg_handler(event):
    msg = event.message.to_dict()['message']
    data = msg.replace(' – ', ', ').split(', ')
    print(data)
    if data != ['']:
        to_whom = await client.get_entity(vinchik)
        is_anket = False
        if 1<len(data):
            is_anket = data[1].isnumeric() and len(data) >=3
        print(is_anket)

        if is_anket:
            if data[2] in cities:
                print('OK')
            else:
                await client.send_message(entity=to_whom, message='👎')
        elif data != [''] and data != ['✨🔍']:
            print('Получено системное сообщение. Выберите ответ вручную на Вашем устройстве.')
        time.sleep(10)
        # if len(data) == 3 or len(data) == 4:
        #    await client.send_message(entity = to_whom, message='👎')
        # await client.log_out()
        # client.disconnect()


@client.on(events.NewMessage(chats='schpecc'))
async def msg_handler(event):
    await client.log_out()
    client.disconnect()

def _phone():
    return input('Дай телефон мразота\n')
def get_code():
    return input('Дай код гандон\n')

client.start(phone = _phone, code_callback=get_code)

client.run_until_disconnected()


