from flask import Flask, jsonify, render_template, redirect, url_for, session, request
from flask_session import Session
from telethon import events
from telethon import TelegramClient
import time
#flask stuff
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
#telethon stuff
api_id = 20387754
api_hash = 'c47bb9cdd6c140651113f118ae27d79f'
vinchik = 'leomatchbot'
client = TelegramClient('session_name', api_id, api_hash)

@app.route("/logout")
def logout():
    session["tel"] = None
    return redirect("/login")

@app.route('/success', methods=['GET', 'POST'])
def success():
    def Get_Code():
        code = request.form.get("code")
        return code
    if not session.get("tel"):
        return redirect("/login")
        
    if request.method == 'GET':
        client.start(phone=session.get("tel"), code_callback=Get_Code)
        tel = session['tel']
        return render_template('index.html', form = 'code')
    #if request.method == 'POST':

    
    #client.start(phone=session.get("tel"), fn)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # GET request
    if request.method == 'GET':
        return render_template('index.html', form = 'phone')


    #функция, вызывает всплывающее окно для ввода телефона. Возвращает телефон
    #функция, вызывает в.о. для ввода кода. Возвращает код
    #client.start(сюда передаются две верхние функции)


    # POST request
    if request.method == 'POST':
        # Session start, ввод телефона для получения кода
        session['tel'] = request.form.get("tel")
        return redirect(url_for('success'))
