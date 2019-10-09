from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name, URL
from telebot.ai import generate_smart_reply
import re
from time import sleep
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    print(update.message)
    chat_id = update.message.chat.id
   
    msg_id = update.message.message_id

    text = update.message.text.encode('utf-8').decode()
    print('got text message:', text)
    reply = generate_smart_reply(text)
    bot.sendMessage(chat_id=chat_id, text=reply, reply_to_message_id=msg_id)

    if text == '/start':
        bot_welcome = """Welcome to Mama Africa Vacation Channel."""
        bot.sendChatAction(chat_id=chat_id, action="typing")
        sleep(1.5)
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    else: 
        try:
            text = re.sub(r"\W", "_", text)
            url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
            bot.sendChatAction(chat_id=chat_id, action="upload_photo")
            sleep(2)
            bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
        except Exception:
            bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)
    
    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(threaded=True)