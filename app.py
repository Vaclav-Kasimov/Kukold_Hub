import base64
import os
import time

from quart import Quart, render_template_string, render_template, request, redirect, make_response

from telethon import TelegramClient, utils
from telethon.errors import SessionPasswordNeededError

import search

def get_env(name, message):
    if name in os.environ:
        return os.environ[name]
    return input(message)


BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset='UTF-8'>
        <title>Telethon + Quart</title>
    </head>
    <body>{{ content | safe }}</body>
</html>
'''

PHONE_FORM = '''
<form action='/' method='post'>
    Phone (international format): <input name='phone' type='text' placeholder='+34600000000'>
    <input type='submit'>
</form>
'''

CODE_FORM = '''
<form action='/' method='post'>
    Telegram code: <input name='code' type='text' placeholder='70707'>
    <input type='submit'>
</form>
'''

PASSWORD_FORM = '''
<form action='/' method='post'>
    Telegram password: <input name='password' type='text' placeholder='your password'>
    <input type='submit'>
</form>
'''

CONTENT_FORM = '''
<form action='/' method='post'>
    <input name='age' type='text' placeholder='минимальный возраст'>
    <input name='city' type='text' placeholder='город'>
    <select name="like_option" id="like_optioin">
        <optgroup label="При соответствии параметром">
            <option value="auto">Ставить лайк автоматически</option>
            <option value="pause">Остановить поиск</option>
        </optgroup>
    </select>
    <button name='start' type='submit'>Старт</button>
    <button name='stop' type='submit'>Стоп</button>
</form>
'''

# Session name, API ID and hash to use; loaded from environmental variables
SESSION = os.environ.get('TG_SESSION', 'quart')
API_ID = '20387754'
API_HASH = 'c47bb9cdd6c140651113f118ae27d79f'

# Telethon client
client = TelegramClient(SESSION, API_ID, API_HASH)
client.parse_mode = 'html'  # <- Render things nicely
phone = None

# Quart app
app = Quart(__name__)
app.secret_key = 'CHANGE THIS TO SOMETHING SECRET'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Helper method to format messages nicely
async def format_message(message):
    if message.photo:
        content = '<img src="data:image/png;base64,{}" alt="{}" />'.format(
            base64.b64encode(await message.download_media(bytes)).decode(),
            message.raw_text
        )
    else:
        # client.parse_mode = 'html', so bold etc. will work!
        content = (message.text or '(action message)').replace('\n', '<br>')

    return '<p><strong>{}</strong>: {}<sub>{}</sub></p>'.format(
        utils.get_display_name(message.sender),
        content,
        message.date
    )


# Connect the client before we start serving with Quart
@app.before_serving
async def startup():
    # After connecting, the client will create additional asyncio tasks that run until it's disconnected again.
    # Be careful to not mix different asyncio loops during a client's lifetime, or things won't work properly!
    await client.connect()


# After we're done serving (near shutdown), clean up the client
@app.after_serving
async def cleanup():
    await client.disconnect()

@app.route('/xyu')
async def xyu():
    response = await make_response({"Pidor": "pidoras"})
    time.sleep(3)
    return response
    
@app.route('/logged', methods=['GET', 'POST'])
async def logged():
    # if request.method == 'POST':
    #     def aa(): 
    #         return 'asdasd'
    #     return await aa()
    if await client.is_user_authorized():
        return await render_template('index.html', form="search-form")
    else:
        return await redirect('/')


@app.route('/', methods=['GET', 'POST'])
async def root():
    # We want to update the global phone variable to remember it
    global phone
    global city
    global age
    global like_option

    # Check form parameters (phone/code)
    form = await request.form
    if 'phone' in form:
        phone = form['phone']
        await client.send_code_request(phone)

    if 'code' in form:
        try:
            await client.sign_in(code=form['code'])
        except SessionPasswordNeededError:
            return await render_template_string(BASE_TEMPLATE, content=PASSWORD_FORM)

    if 'password' in form:
        await client.sign_in(password=form['password'])

    # If we're logged in, show them some messages from their first dialog
    if await client.is_user_authorized():
        return redirect('/logged')

    # Ask for the phone if we don't know it yet
    if phone is None:
        return await render_template_string(BASE_TEMPLATE, content=PHONE_FORM)

    # We have the phone, but we're not logged in, so ask for the code
    return await render_template_string(BASE_TEMPLATE, content=CODE_FORM)


# By default, `Quart.run` uses `asyncio.run()`, which creates a new asyncio
# event loop. If we had connected the `TelegramClient` before, `telethon` will
# use `asyncio.get_running_loop()` to create some additional tasks. If these
# loops are different, it won't work.
#
# To keep things simple, be sure to not create multiple asyncio loops!
if __name__ == '__main__':
    app.run()