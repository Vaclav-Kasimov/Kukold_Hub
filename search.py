import time, random, json
from telethon import TelegramClient, events
def FindGirl(age, cities, like_option, client):

    if like_option == 'pause':
        doPause = True
    else:
        doPause = False
    cities = cities.split(', ')
    vinchik = 'leomatchbot'
    @client.on(events.NewMessage(chats=vinchik, incoming=True))
    async def msg_handler(event):
        msg = event.message.to_dict()['message']
        data = msg.replace(' – ', ', ').split(', ')
        print(data)
        if data != ['']:
            to_whom = await client.get_entity(vinchik)
            is_anket = False

            if 1 < len(data):
                is_anket = data[1].isnumeric() and len(data) >= 3

            if not is_anket:
                print('Это не анкета')

            if is_anket:
                print('Это анкета')
                if data[2] in cities and int(data[1]) >= int(age):
                    print('OK')
                    if doPause:
                        print('Girl found')
                        return('Найдена удовлетворяющая запросу анкета. Выберете дальнейшее действие на Вашем устройстве вручную.')
                    else:
                        print('Sent Like, continuing parsing...')
                        await client.send_message(entity=to_whom, message='2')
                        time.sleep(1)
                        await client.send_message(entity=to_whom, message=make_complmient(data[0]))
                else:
                    await client.send_message(entity=to_whom, message='👎')
                    print('bruh')

            elif data != [''] and data != ['✨🔍'] and data.find('Нашли кое-кого для тебя') != -1 and data.find('Есть взаимная симпатия') != -1:
                print('SystemMessage recieved')
                return('Получено системное сообщение. Выберите ответ вручную на Вашем устройстве.')
            time.sleep(random.randint(5,15))


def make_complmient(name):
    with open('compliments.json', 'r') as compliments:
        compliments_list = json.load(compliments)
    compliment = compliments_list.get(str(random.randint(1,50)))
    return compliment.replace("[name]", name)

async def stopSearch(client):
    await client.log_out()
    client.disconnect()
